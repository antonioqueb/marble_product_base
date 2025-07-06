# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    # Campo para asociar productos de mármol generados
    has_marble_products = fields.Boolean(
        string='Contiene Productos de Mármol',
        compute='_compute_has_marble_products',
        store=True,
        help='Indica si esta transferencia contiene productos generados de mármol'
    )
    
    packing_list_id = fields.Many2one(
        'packing.list.import',
        string='Packing List Asociado',
        help='Packing list del cual se generaron los productos'
    )
    
    marble_reception_complete = fields.Boolean(
        string='Recepción de Mármol Completa',
        default=False,
        help='Indica si la recepción de productos de mármol está completa'
    )
    
    @api.depends('move_ids.product_id.is_generated_marble_product')
    def _compute_has_marble_products(self):
        """Determinar si contiene productos de mármol"""
        for picking in self:
            picking.has_marble_products = any(
                move.product_id.is_generated_marble_product 
                for move in picking.move_ids
            )
    
    def button_validate(self):
        """
        Sobrescribir validación para manejar productos de mármol
        """
        # Procesar lógica específica de mármol antes de la validación estándar
        if self.picking_type_id.code == 'incoming':
            self._handle_marble_incoming_validation()
        elif self.picking_type_id.code == 'outgoing':
            self._handle_marble_outgoing_validation()
        
        # Ejecutar validación estándar
        res = super().button_validate()
        
        # Procesar lógica posterior a la validación
        if self.picking_type_id.code == 'outgoing':
            self._auto_archive_zero_stock_marble_products()
        
        return res
    
    def _handle_marble_incoming_validation(self):
        """
        Manejar validación de entrada de productos de mármol
        """
        marble_moves = self.move_ids.filtered(
            lambda m: m.product_id.is_generated_marble_product
        )
        
        if not marble_moves:
            return
        
        # Validar que todos los productos de mármol tengan número de serie
        for move in marble_moves:
            if move.product_id.tracking == 'serial':
                move_lines_with_lot = move.move_line_ids.filtered(lambda ml: ml.lot_id)
                if not move_lines_with_lot:
                    # Crear automáticamente el lote basado en el número de serie del producto
                    self._create_marble_lot_for_move(move)
    
    def _create_marble_lot_for_move(self, move):
        """
        Crear número de serie automáticamente para productos de mármol
        """
        if not move.product_id.marble_serial_number:
            _logger.warning(f"Producto {move.product_id.name} no tiene número de serie de mármol")
            return
        
        # Buscar si ya existe el lote
        existing_lot = self.env['stock.lot'].search([
            ('product_id', '=', move.product_id.id),
            ('name', '=', move.product_id.marble_serial_number)
        ], limit=1)
        
        if not existing_lot:
            # Crear el lote
            lot = self.env['stock.lot'].create({
                'name': move.product_id.marble_serial_number,
                'product_id': move.product_id.id,
                'company_id': self.company_id.id,
            })
        else:
            lot = existing_lot
        
        # Actualizar las líneas de movimiento
        for move_line in move.move_line_ids:
            if not move_line.lot_id:
                move_line.lot_id = lot.id
        
        _logger.info(f"Lote asignado para producto de mármol: {move.product_id.name} - {lot.name}")
    
    def _handle_marble_outgoing_validation(self):
        """
        Manejar validación de salida de productos de mármol
        """
        marble_moves = self.move_ids.filtered(
            lambda m: m.product_id.is_generated_marble_product
        )
        
        if not marble_moves:
            return
        
        # Cambiar estado de productos que se están vendiendo
        for move in marble_moves:
            if move.product_id.marble_status in ['available', 'reserved']:
                move.product_id.marble_status = 'sold'
                _logger.info(f"Producto de mármol marcado como vendido: {move.product_id.name}")
    
    def _auto_archive_zero_stock_marble_products(self):
        """
        Archivar automáticamente productos de mármol con stock cero después de la salida
        """
        marble_products = self.move_ids.mapped('product_id').filtered(
            lambda p: p.is_generated_marble_product
        )
        
        if not marble_products:
            return
        
        archived_count = 0
        for product in marble_products:
            # Forzar recálculo de stock
            product.invalidate_recordset(['qty_available'])
            
            if product.qty_available <= 0 and product.active:
                product.action_archive_marble_product()
                archived_count += 1
                _logger.info(f"Producto de mármol archivado automáticamente: {product.name}")
        
        if archived_count > 0:
            _logger.info(f"Total productos de mármol archivados: {archived_count}")
    
    def action_view_marble_products(self):
        """Ver productos de mármol en esta transferencia"""
        self.ensure_one()
        marble_products = self.move_ids.mapped('product_id').filtered(
            lambda p: p.is_generated_marble_product
        )
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos de Mármol - {self.name}',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', marble_products.ids)],
            'context': {'create': False}
        }
    
    def action_create_marble_reception(self):
        """
        Crear recepción especial para productos de mármol desde packing list
        """
        self.ensure_one()
        
        if self.picking_type_id.code != 'incoming':
            raise UserError("Esta acción solo está disponible para recepciones.")
        
        if not self.purchase_id:
            raise UserError("Esta transferencia debe estar asociada a una orden de compra.")
        
        # Buscar packing lists de la orden de compra
        packing_lists = self.env['packing.list.import'].search([
            ('purchase_order_id', '=', self.purchase_id.id),
            ('state', '=', 'processed')
        ])
        
        if not packing_lists:
            raise UserError("No hay packing lists procesados para esta orden de compra.")
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seleccionar Packing List',
            'res_model': 'packing.list.import',
            'view_mode': 'list,form',
            'domain': [('id', 'in', packing_lists.ids)],
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
                'select_for_reception': True
            }
        }


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    is_marble_product = fields.Boolean(
        string='Es Producto de Mármol',
        related='product_id.is_generated_marble_product',
        store=True
    )
    
    marble_serial_number = fields.Char(
        string='Número de Serie Mármol',
        related='product_id.marble_serial_number',
        readonly=True
    )
    
    def _action_done(self, cancel_backorder=False):
        """Sobrescribir para manejar lógica específica de mármol"""
        
        # Ejecutar lógica estándar primero
        res = super()._action_done(cancel_backorder=cancel_backorder)
        
        # Procesar productos de mármol
        marble_moves = self.filtered(lambda m: m.is_marble_product)
        
        for move in marble_moves:
            if move.picking_id.picking_type_id.code == 'incoming':
                # Marcar como disponible en recepción
                if move.product_id.marble_status == 'draft':
                    move.product_id.marble_status = 'available'
                    _logger.info(f"Producto de mármol marcado como disponible: {move.product_id.name}")
        
        return res


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    is_marble_product = fields.Boolean(
        string='Es Producto de Mármol',
        related='product_id.is_generated_marble_product',
        store=True
    )
    
    marble_dimensions = fields.Char(
        string='Dimensiones',
        compute='_compute_marble_dimensions',
        help='Dimensiones de la placa de mármol'
    )
    
    @api.depends('product_id.marble_height', 'product_id.marble_width', 'product_id.marble_thickness')
    def _compute_marble_dimensions(self):
        """Calcular cadena de dimensiones"""
        for line in self:
            if line.is_marble_product and line.product_id:
                height = line.product_id.marble_height
                width = line.product_id.marble_width
                thickness = line.product_id.marble_thickness
                
                if height and width and thickness:
                    line.marble_dimensions = f"{height:.1f} x {width:.1f} x {thickness:.1f} cm"
                else:
                    line.marble_dimensions = "Dimensiones no definidas"
            else:
                line.marble_dimensions = ""