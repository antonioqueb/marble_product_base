# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    # Campos adicionales para el manejo de mármol
    has_marble_products = fields.Boolean(
        string='Contiene Productos de Mármol',
        compute='_compute_has_marble_products',
        store=True,
        help='Indica si esta orden contiene productos de mármol'
    )
    
    packing_list_imported = fields.Boolean(
        string='Packing List Importado',
        default=False,
        help='Indica si ya se importó el packing list para esta orden'
    )
    
    container_number = fields.Char(
        string='Número de Contenedor',
        help='Número del contenedor asociado a esta orden'
    )
    
    commercial_invoice = fields.Char(
        string='Factura Comercial',
        help='Número de factura comercial del proveedor'
    )
    
    # Campos de seguimiento del proceso
    packing_list_count = fields.Integer(
        string='Packing Lists',
        compute='_compute_packing_list_count',
        help='Número de packing lists importados'
    )
    
    generated_products_count = fields.Integer(
        string='Productos Generados',
        compute='_compute_generated_products_count',
        help='Número de productos únicos generados'
    )
    
    # Totales calculados
    total_marble_sqm = fields.Float(
        string='Total M² Mármol',
        compute='_compute_marble_totals',
        store=True,
        digits=(10, 4),
        help='Total de metros cuadrados de mármol en la orden'
    )
    
    @api.depends('order_line.product_id.is_marble_template')
    def _compute_has_marble_products(self):
        """Determinar si la orden contiene productos de mármol"""
        for order in self:
            order.has_marble_products = any(
                line.product_id.is_marble_template for line in order.order_line
            )
    
    def _compute_packing_list_count(self):
        """Contar packing lists importados"""
        for order in self:
            packing_lists = self.env['packing.list.import'].search([
                ('purchase_order_id', '=', order.id)
            ])
            order.packing_list_count = len(packing_lists)
    
    def _compute_generated_products_count(self):
        """Contar productos generados"""
        for order in self:
            # Buscar productos generados a través de packing lists
            packing_lists = self.env['packing.list.import'].search([
                ('purchase_order_id', '=', order.id)
            ])
            generated_products = self.env['product.product'].search([
                ('packing_list_import_line_id', 'in', packing_lists.line_ids.ids)
            ])
            order.generated_products_count = len(generated_products)
    
    @api.depends('order_line.product_qty', 'order_line.product_id.is_marble_template')
    def _compute_marble_totals(self):
        """Calcular totales de metros cuadrados de mármol"""
        for order in self:
            total_sqm = 0
            for line in order.order_line:
                if line.product_id.is_marble_template:
                    total_sqm += line.product_qty
            order.total_marble_sqm = total_sqm
    
    def action_import_packing_list(self):
        """Abrir wizard para importar packing list"""
        self.ensure_one()
        
        if not self.has_marble_products:
            raise UserError("Esta orden no contiene productos de mármol.")
        
        if self.state not in ['purchase', 'done']:
            raise UserError("La orden debe estar confirmada para importar el packing list.")
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Importar Packing List',
            'res_model': 'packing.list.import.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_purchase_order_id': self.id,
                'default_container_number': self.container_number,
                'default_commercial_invoice': self.commercial_invoice,
            }
        }
    
    def action_view_packing_lists(self):
        """Ver packing lists de esta orden"""
        self.ensure_one()
        packing_lists = self.env['packing.list.import'].search([
            ('purchase_order_id', '=', self.id)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Packing Lists - {self.name}',
            'res_model': 'packing.list.import',
            'view_mode': 'list,form',
            'domain': [('id', 'in', packing_lists.ids)],
            'context': {'default_purchase_order_id': self.id}
        }
    
    def action_view_generated_products(self):
        """Ver productos generados desde esta orden"""
        self.ensure_one()
        packing_lists = self.env['packing.list.import'].search([
            ('purchase_order_id', '=', self.id)
        ])
        generated_products = self.env['product.product'].search([
            ('packing_list_import_line_id', 'in', packing_lists.line_ids.ids)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos Generados - {self.name}',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', generated_products.ids)],
            'context': {'create': False}
        }
    
    def button_confirm(self):
        """Sobrescribir confirmación para validar datos de mármol"""
        # Validar datos de mármol antes de confirmar
        for line in self.order_line:
            if line.product_id.is_marble_template:
                if not line.product_qty or line.product_qty <= 0:
                    raise ValidationError(
                        f"La cantidad debe ser mayor a cero para el producto de mármol: {line.product_id.name}"
                    )
        
        return super().button_confirm()


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    # Campos temporales para captura de datos del mármol
    marble_height = fields.Float(
        string='Alto (cm)',
        digits=(10, 2),
        help='Alto promedio de las placas en centímetros'
    )
    
    marble_width = fields.Float(
        string='Ancho (cm)',
        digits=(10, 2), 
        help='Ancho promedio de las placas en centímetros'
    )
    
    marble_thickness = fields.Float(
        string='Grosor (cm)',
        digits=(10, 2),
        help='Grosor de las placas en centímetros'
    )
    
    marble_custom_lot = fields.Char(
        string='Lote General',
        help='Lote general para agrupar las placas de esta línea'
    )
    
    marble_finish = fields.Char(
        string='Acabado',
        help='Acabado del mármol (Pulido, Leather, etc.)'
    )
    
    # Campos calculados
    estimated_pieces = fields.Integer(
        string='Piezas Estimadas',
        help='Número estimado de piezas basado en m² promedio'
    )
    
    avg_sqm_per_piece = fields.Float(
        string='M² Promedio por Pieza',
        compute='_compute_avg_sqm_per_piece',
        store=True,
        digits=(10, 4),
        help='Metros cuadrados promedio por pieza'
    )
    
    @api.depends('marble_height', 'marble_width')
    def _compute_avg_sqm_per_piece(self):
        """Calcular metros cuadrados promedio por pieza"""
        for line in self:
            if line.marble_height and line.marble_width:
                line.avg_sqm_per_piece = (line.marble_height * line.marble_width) / 10000
            else:
                line.avg_sqm_per_piece = 0.0
    
    @api.onchange('product_id')
    def _onchange_product_id_marble(self):
        """Configurar campos específicos cuando se selecciona una plantilla de mármol"""
        if self.product_id and self.product_id.is_marble_template:
            # Copiar valores por defecto de la plantilla
            self.marble_thickness = self.product_id.marble_thickness
            self.marble_finish = self.product_id.marble_finish
            # Configurar unidad de medida a metros cuadrados
            sqm_uom = self.env.ref('uom.product_uom_meter', raise_if_not_found=False)
            if sqm_uom:
                self.product_uom = sqm_uom
    
    @api.onchange('product_qty', 'avg_sqm_per_piece')
    def _onchange_estimate_pieces(self):
        """Estimar número de piezas basado en cantidad total y m² promedio"""
        if self.product_qty and self.avg_sqm_per_piece and self.avg_sqm_per_piece > 0:
            self.estimated_pieces = int(self.product_qty / self.avg_sqm_per_piece)
        else:
            self.estimated_pieces = 0
    
    @api.constrains('marble_height', 'marble_width', 'marble_thickness')
    def _check_marble_dimensions(self):
        """Validar dimensiones de mármol"""
        for line in self:
            if line.product_id.is_marble_template:
                if line.marble_height and line.marble_height <= 0:
                    raise ValidationError("El alto debe ser mayor a cero.")
                if line.marble_width and line.marble_width <= 0:
                    raise ValidationError("El ancho debe ser mayor a cero.")
                if line.marble_thickness and line.marble_thickness <= 0:
                    raise ValidationError("El grosor debe ser mayor a cero.")