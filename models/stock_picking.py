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
    
    # ✅ NUEVO CAMPO para controlar si ya se aplicaron los productos del packing list
    packing_list_applied = fields.Boolean(
        string='Packing List Aplicado',
        default=False,
        help='Indica si los productos del packing list ya fueron aplicados a esta recepción'
    )
    
    @api.depends('move_ids.product_id.is_generated_marble_product')
    def _compute_has_marble_products(self):
        """Determinar si contiene productos de mármol"""
        for picking in self:
            picking.has_marble_products = any(
                move.product_id.is_generated_marble_product 
                for move in picking.move_ids
            )
    
    # ✅ MÉTODO CORREGIDO para Odoo 18
    def action_apply_packing_list_products(self):
        """
        Aplicar productos únicos del packing list a esta recepción
        Reemplaza las líneas de plantillas con productos específicos
        """
        self.ensure_one()
        
        if not self.purchase_id:
            raise UserError("Esta transferencia debe estar asociada a una orden de compra.")
        
        if self.packing_list_applied:
            raise UserError("Los productos del packing list ya han sido aplicados a esta recepción.")
        
        # Buscar packing lists procesados de la orden de compra
        packing_lists = self.env['packing.list.import'].search([
            ('purchase_order_id', '=', self.purchase_id.id),
            ('state', '=', 'processed')
        ])
        
        if not packing_lists:
            raise UserError("No hay packing lists procesados para esta orden de compra.")
        
        # Obtener todos los productos únicos creados desde los packing lists
        generated_products = self.env['product.product'].search([
            ('packing_list_import_line_id', 'in', packing_lists.line_ids.ids)
        ])
        
        if not generated_products:
            raise UserError("No se encontraron productos únicos generados desde los packing lists.")
        
        # Eliminar movimientos existentes de plantillas de mármol
        marble_template_moves = self.move_ids.filtered(
            lambda m: m.product_id.is_marble_template
        )
        
        if marble_template_moves:
            # Cancelar primero los movimientos existentes
            marble_template_moves.filtered(lambda m: m.state not in ['done', 'cancel'])._action_cancel()
            # Eliminar los movimientos cancelados
            marble_template_moves.unlink()
        
        # Crear nuevos movimientos para cada producto único
        for product in generated_products:
            # Verificar que el producto tenga un lote/número de serie
            lot = self.env['stock.lot'].search([
                ('product_id', '=', product.id),
                ('name', '=', product.marble_serial_number)
            ], limit=1)
            
            if not lot:
                # Crear el lote si no existe
                lot = self.env['stock.lot'].create({
                    'name': product.marble_serial_number,
                    'product_id': product.id,
                    'company_id': self.company_id.id,
                })
            
            # Crear movimiento de stock para este producto
            move_vals = {
                'name': f"Recepción: {product.name}",
                'product_id': product.id,
                'product_uom_qty': 1,  # Siempre 1 unidad por producto único
                'product_uom': product.uom_id.id,
                'picking_id': self.id,
                'picking_type_id': self.picking_type_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'state': 'assigned',  # Ya está listo para validar
                'company_id': self.company_id.id,
                'purchase_line_id': self._find_matching_purchase_line(product),
            }
            
            move = self.env['stock.move'].create(move_vals)
            
            # ✅ CORRECCIÓN: Usar campos correctos para Odoo 18
            move_line_vals = {
                'move_id': move.id,
                'product_id': product.id,
                'product_uom_id': product.uom_id.id,
                'quantity': 1,  # ✅ Cambiado de 'qty_done' a 'quantity'
                'lot_id': lot.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'picking_id': self.id,
                'company_id': self.company_id.id,
            }
            
            move_line = self.env['stock.move.line'].create(move_line_vals)
            
            # ✅ NUEVO: Asegurar que el movimiento tenga la cantidad correcta
            move.quantity = 1
            
            _logger.info(f"Movimiento creado para producto único: {product.name} con lote: {lot.name}")
        
        # Marcar como aplicado
        self.packing_list_applied = True
        self.packing_list_id = packing_lists[0].id  # Asociar el primer packing list
        
        # Actualizar estado de los productos a 'draft' si están en otro estado
        generated_products.filtered(lambda p: p.marble_status != 'draft').write({'marble_status': 'draft'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': f"Se aplicaron {len(generated_products)} productos únicos de mármol a la recepción.",
                'type': 'success',
                'sticky': False,
            }
        }
    
    def _find_matching_purchase_line(self, product):
        """Encontrar la línea de compra correspondiente para un producto único"""
        if not self.purchase_id or not product.marble_parent_template_id:
            return False
        
        # Buscar línea de compra que tenga la plantilla padre
        purchase_line = self.purchase_id.order_line.filtered(
            lambda l: l.product_id.id == product.marble_parent_template_id.id
        )
        
        return purchase_line[0].id if purchase_line else False
    
    def button_validate(self):
        """
        Sobrescribir validación para manejar productos de mármol
        """
        # ✅ VERIFICAR si hay productos de packing list pendientes de aplicar
        if self.picking_type_id.code == 'incoming' and self.purchase_id:
            # Verificar si hay packing lists procesados pero no aplicados
            if self._has_processed_packing_lists() and not self.packing_list_applied:
                # Auto-aplicar productos del packing list
                try:
                    self.action_apply_packing_list_products()
                except Exception as e:
                    _logger.warning(f"No se pudieron aplicar automáticamente los productos del packing list: {str(e)}")
        
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
    
    def _has_processed_packing_lists(self):
        """Verificar si hay packing lists procesados para esta orden de compra"""
        if not self.purchase_id:
            return False
        
        packing_lists = self.env['packing.list.import'].search([
            ('purchase_order_id', '=', self.purchase_id.id),
            ('state', '=', 'processed')
        ])
        
        return len(packing_lists) > 0
    
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