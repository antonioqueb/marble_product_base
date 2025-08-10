# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PackingListImport(models.Model):
    _name = 'packing.list.import'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Importación de Packing List'
    _order = 'create_date desc'
    _rec_name = 'display_name'
    
    name = fields.Char(
        string='Referencia',
        required=True,
        default='Nuevo Packing List',
        help='Referencia interna del packing list'
    )
    
    display_name = fields.Char(
        string='Nombre',
        compute='_compute_display_name',
        store=True
    )
    
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de Compra',
        required=True,
        ondelete='cascade',
        domain="[('has_marble_products', '=', True)]"
    )
    
    container_number = fields.Char(
        string='Número de Contenedor',
        required=True,
        help='Número del contenedor del packing list'
    )
    
    commercial_invoice = fields.Char(
        string='Factura Comercial',
        required=True,
        help='Número de factura comercial del proveedor'
    )
    
    supplier_id = fields.Many2one(
        'res.partner',
        string='Proveedor',
        related='purchase_order_id.partner_id',
        store=True,
        readonly=True
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('imported', 'Importado'),
        ('processed', 'Procesado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', tracking=True)
    
    line_ids = fields.One2many(
        'packing.list.import.line',
        'packing_list_id',
        string='Líneas del Packing List'
    )
    
    import_date = fields.Datetime(
        string='Fecha de Importación',
        readonly=True
    )
    
    process_date = fields.Datetime(
        string='Fecha de Procesamiento',
        readonly=True
    )
    
    total_pieces = fields.Integer(
        string='Total de Piezas',
        compute='_compute_totals',
        store=True
    )
    
    total_sqm = fields.Float(
        string='Total M²',
        compute='_compute_totals',
        store=True,
        digits=(10, 4)
    )
    
    total_lots = fields.Integer(
        string='Total de Lotes',
        compute='_compute_totals',
        store=True
    )
    
    total_crates = fields.Integer(
        string='Total de Atados',
        compute='_compute_totals',
        store=True
    )
    
    created_products_count = fields.Integer(
        string='Productos Creados',
        compute='_compute_created_products_count'
    )
    
    notes = fields.Text(
        string='Notas'
    )
    
    @api.depends('name', 'container_number', 'purchase_order_id.name')
    def _compute_display_name(self):
        for record in self:
            parts = [record.name, record.purchase_order_id.name, record.container_number]
            record.display_name = " - ".join(filter(None, parts))

    @api.depends('line_ids.marble_sqm', 'line_ids.marble_custom_lot', 'line_ids.wooden_crate_code')
    def _compute_totals(self):
        for record in self:
            record.total_pieces = len(record.line_ids)
            record.total_sqm = sum(record.line_ids.mapped('marble_sqm'))
            record.total_lots = len(record.line_ids.mapped('marble_custom_lot'))
            record.total_crates = len(record.line_ids.mapped('wooden_crate_code'))
    
    def _compute_created_products_count(self):
        for record in self:
            record.created_products_count = self.env['product.product'].search_count([
                ('packing_list_import_line_id', 'in', record.line_ids.ids)
            ])
    
    def action_process_packing_list(self):
        self.ensure_one()
        if self.state != 'imported':
            raise UserError("Solo se pueden procesar packing lists importados.")
        if not self.line_ids:
            raise UserError("No hay líneas para procesar.")

        created_products = self.env['product.product']
        for line in self.line_ids:
            template = self._find_marble_template(line.product_name)
            if not template:
                raise UserError(f"No se encontró plantilla para: {line.product_name}")
            
            marble_data = {
                'marble_height': line.marble_height,
                'marble_width': line.marble_width,
                'marble_thickness': line.marble_thickness,
                'marble_custom_lot': line.marble_custom_lot,
                'wooden_crate_code': line.wooden_crate_code,
                'container_number': self.container_number,
                'commercial_invoice': self.commercial_invoice,
                'supplier_lot_number': line.supplier_lot_number,
                'cost_price': line.cost_price,
                'price_per_sqm': line.price_per_sqm,
                'marble_finish': line.marble_finish,
            }
            product = self.env['product.product'].create_marble_product_from_template(template.id, marble_data, line.id)
            line.created_product_id = product.id
            created_products |= product

        self.write({
            'state': 'processed',
            'process_date': fields.Datetime.now()
        })
        self.purchase_order_id.packing_list_imported = True
        self._notify_pending_receptions()
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos Creados ({len(created_products)})',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created_products.ids)],
        }
    
    def _notify_pending_receptions(self):
        pending_pickings = self.env['stock.picking'].search([
            ('purchase_id', '=', self.purchase_order_id.id),
            ('picking_type_id.code', '=', 'incoming'),
            ('state', 'in', ['assigned', 'confirmed', 'waiting']),
            ('packing_list_applied', '=', False)
        ])
        if pending_pickings:
            for picking in pending_pickings:
                picking.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=f'Aplicar productos de packing list - {self.display_name}',
                    note=f'El packing list {self.display_name} ha sido procesado. Use el botón "Aplicar Productos de Packing List" en la recepción {picking.name} para continuar.',
                    user_id=self.env.user.id
                )
    
    def _find_marble_template(self, product_name):
        if not product_name: return None
        domain = [('is_marble_template', '=', True), ('name', 'ilike', product_name)]
        template = self.env['product.template'].search(domain, limit=1)
        if not template:
            base_name = product_name.split('-')[0].strip()
            domain = [('is_marble_template', '=', True), ('name', 'ilike', base_name)]
            template = self.env['product.template'].search(domain, limit=1)
        return template
    
    def action_view_created_products(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos Creados - {self.display_name}',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('packing_list_import_line_id', 'in', self.line_ids.ids)],
            'context': {'create': False}
        }
    
    def action_cancel(self):
        self.ensure_one()
        if self.state == 'processed':
            raise UserError("No se puede cancelar un packing list ya procesado.")
        self.state = 'cancelled'
    
    def action_set_to_draft(self):
        self.ensure_one()
        if self.state == 'processed':
            raise UserError("No se puede volver a borrador un packing list procesado.")
        self.state = 'draft'


class PackingListImportLine(models.Model):
    _name = 'packing.list.import.line'
    _description = 'Línea de Importación de Packing List'
    _order = 'marble_custom_lot, wooden_crate_code, supplier_lot_number'
    
    packing_list_id = fields.Many2one(
        'packing.list.import',
        string='Packing List',
        required=True,
        ondelete='cascade'
    )
    
    product_name = fields.Char(
        string='Nombre del Producto',
        required=True,
        help='Nombre del material del packing list'
    )
    
    marble_height = fields.Float(
        string='Alto (cm)',
        required=True,
        digits=(10, 2)
    )
    
    marble_width = fields.Float(
        string='Ancho (cm)',
        required=True,
        digits=(10, 2)
    )
    
    marble_thickness = fields.Float(
        string='Grosor (cm)',
        required=True,
        digits=(10, 2)
    )
    
    marble_sqm = fields.Float(
        string='M²',
        compute='_compute_marble_sqm',
        store=True,
        digits=(10, 4)
    )
    
    # ✅ ETIQUETA CORREGIDA: Cambio de "Lote Personalizado" a "Lote"
    marble_custom_lot = fields.Char(
        string='Lote',
        required=True,
        help='Lote personalizado para agrupar placas'
    )
    
    wooden_crate_code = fields.Char(
        string='Código de Atado',
        required=True,
        help='Wooden Crate Code del packing list'
    )
    
    supplier_lot_number = fields.Char(
        string='Número de Lote Proveedor',
        required=True,
        help='Número de serie del proveedor (Lot del packing list)'
    )
    
    marble_finish = fields.Char(
        string='Acabado',
        help='Acabado del mármol extraído del nombre del producto'
    )
    
    cost_price = fields.Float(
        string='Costo',
        digits='Product Price',
        help='Costo unitario de la placa'
    )
    
    price_per_sqm = fields.Float(
        string='Precio por M²',
        digits='Product Price',
        help='Precio por metro cuadrado'
    )
    
    created_product_id = fields.Many2one(
        'product.product',
        string='Producto Creado',
        readonly=True,
        help='Producto único generado desde esta línea'
    )
    
    is_processed = fields.Boolean(
        string='Procesado',
        compute='_compute_is_processed',
        store=True
    )
    
    has_errors = fields.Boolean(
        string='Tiene Errores',
        default=False
    )
    
    error_message = fields.Text(
        string='Mensaje de Error'
    )
    
    @api.depends('marble_height', 'marble_width')
    def _compute_marble_sqm(self):
        for record in self:
            if record.marble_height and record.marble_width:
                record.marble_sqm = (record.marble_height * record.marble_width) / 10000
            else:
                record.marble_sqm = 0.0
    
    @api.depends('created_product_id')
    def _compute_is_processed(self):
        for record in self:
            record.is_processed = bool(record.created_product_id)
    
    @api.onchange('product_name')
    def _onchange_product_name(self):
        if self.product_name:
            name_parts = self.product_name.split('-')
            if len(name_parts) > 1:
                finishes = ['Leather', 'Polished', 'Honed', 'Brushed', 'Antique']
                for part in name_parts:
                    if any(finish.lower() in part.lower() for finish in finishes):
                        self.marble_finish = part.strip()
                        break
    
    @api.constrains('marble_height', 'marble_width', 'marble_thickness')
    def _check_dimensions(self):
        for record in self:
            if record.marble_height <= 0:
                raise ValidationError("El alto debe ser mayor a cero.")
            if record.marble_width <= 0:
                raise ValidationError("El ancho debe ser mayor a cero.")
            if record.marble_thickness <= 0:
                raise ValidationError("El grosor debe ser mayor a cero.")
    
    def action_view_created_product(self):
        self.ensure_one()
        if not self.created_product_id:
            raise UserError("Esta línea no ha sido procesada aún.")
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Producto Creado',
            'res_model': 'product.product',
            'res_id': self.created_product_id.id,
            'view_mode': 'form',
            'target': 'current'
        }