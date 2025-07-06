# -*- coding: utf-8 -*-

from odoo import models, fields, api
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
        domain=[('has_marble_products', '=', True)]
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
    
    # Líneas del packing list
    line_ids = fields.One2many(
        'packing.list.import.line',
        'packing_list_id',
        string='Líneas del Packing List'
    )
    
    # Fechas importantes
    import_date = fields.Datetime(
        string='Fecha de Importación',
        readonly=True
    )
    
    process_date = fields.Datetime(
        string='Fecha de Procesamiento',
        readonly=True
    )
    
    # Resumen estadístico
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
    
    # Productos creados
    created_products_count = fields.Integer(
        string='Productos Creados',
        compute='_compute_created_products_count'
    )
    
    # Campos de control
    notes = fields.Text(
        string='Notas'
    )
    
    @api.depends('name', 'container_number', 'purchase_order_id.name')
    def _compute_display_name(self):
        """Generar nombre de visualización"""
        for record in self:
            if record.purchase_order_id:
                record.display_name = f"{record.name} - {record.purchase_order_id.name} - {record.container_number}"
            else:
                record.display_name = record.name
    
    @api.depends('line_ids.marble_sqm', 'line_ids.marble_custom_lot', 'line_ids.wooden_crate_code')
    def _compute_totals(self):
        """Calcular totales estadísticos"""
        for record in self:
            record.total_pieces = len(record.line_ids)
            record.total_sqm = sum(record.line_ids.mapped('marble_sqm'))
            record.total_lots = len(set(record.line_ids.mapped('marble_custom_lot'))) if record.line_ids else 0
            record.total_crates = len(set(record.line_ids.mapped('wooden_crate_code'))) if record.line_ids else 0
    
    def _compute_created_products_count(self):
        """Contar productos creados"""
        for record in self:
            created_products = self.env['product.product'].search([
                ('packing_list_import_line_id', 'in', record.line_ids.ids)
            ])
            record.created_products_count = len(created_products)
    
    def action_process_packing_list(self):
        """Procesar el packing list y crear los productos únicos"""
        self.ensure_one()
        
        if self.state != 'imported':
            raise UserError("Solo se pueden procesar packing lists importados.")
        
        if not self.line_ids:
            raise UserError("No hay líneas para procesar.")
        
        created_products = []
        errors = []
        
        # Procesar cada línea
        for line in self.line_ids:
            try:
                # Buscar la plantilla de mármol correspondiente
                template = self._find_marble_template(line.product_name)
                
                if not template:
                    error_msg = f"No se encontró plantilla para: {line.product_name}"
                    errors.append(error_msg)
                    continue
                
                # Preparar datos para crear el producto
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
                
                # Crear el producto único
                product = self.env['product.product'].create_marble_product_from_template(
                    template.id, marble_data, line.id
                )
                
                created_products.append(product)
                
                # Actualizar la línea con el producto creado
                line.created_product_id = product.id
                
                _logger.info(f"Producto creado: {product.name}")
                
            except Exception as e:
                error_msg = f"Error procesando línea {line.supplier_lot_number}: {str(e)}"
                errors.append(error_msg)
                _logger.error(error_msg)
        
        # Actualizar fechas y estado
        self.process_date = fields.Datetime.now()
        
        if errors:
            # Si hay errores, mostrarlos al usuario
            error_message = "Se encontraron los siguientes errores:\n" + "\n".join(errors)
            if created_products:
                error_message += f"\n\nSe crearon {len(created_products)} productos exitosamente."
            raise UserError(error_message)
        
        # Si todo salió bien, marcar como procesado
        self.state = 'processed'
        self.purchase_order_id.packing_list_imported = True
        
        # ✅ NUEVA FUNCIONALIDAD: Notificar a las recepciones pendientes
        self._notify_pending_receptions()
        
        # Mostrar productos creados
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos Creados ({len(created_products)})',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', [p.id for p in created_products])],
            'context': {'create': False}
        }
    
    # ✅ NUEVO MÉTODO para notificar recepciones pendientes
    def _notify_pending_receptions(self):
        """Notificar a las recepciones pendientes que hay productos de packing list disponibles"""
        # Buscar recepciones pendientes de esta orden de compra
        pending_pickings = self.env['stock.picking'].search([
            ('purchase_id', '=', self.purchase_order_id.id),
            ('picking_type_id.code', '=', 'incoming'),
            ('state', 'in', ['assigned', 'confirmed', 'waiting']),
            ('packing_list_applied', '=', False)
        ])
        
        if pending_pickings:
            # Crear actividad para recordar aplicar los productos
            for picking in pending_pickings:
                picking.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=f'Aplicar productos de packing list - {self.display_name}',
                    note=f'''
                        El packing list {self.display_name} ha sido procesado y los productos únicos están listos.
                        
                        Use el botón "Aplicar Productos de Packing List" en la recepción {picking.name} 
                        para reemplazar las plantillas con los productos específicos antes de validar.
                        
                        Productos generados: {len(self.line_ids)} placas únicas
                    ''',
                    user_id=self.env.user.id
                )
            
            _logger.info(f"Notificadas {len(pending_pickings)} recepciones pendientes para aplicar productos del packing list {self.display_name}")
    
    def _find_marble_template(self, product_name):
        """
        Buscar la plantilla de mármol correspondiente al nombre del producto
        
        Args:
            product_name (str): Nombre del producto del packing list
            
        Returns:
            product.template: Plantilla encontrada o None
        """
        # Lógica de búsqueda mejorada
        if not product_name:
            return None
        
        # 1. Buscar por coincidencia exacta
        templates = self.env['product.template'].search([
            ('is_marble_template', '=', True),
            ('name', '=', product_name)
        ], limit=1)
        
        if templates:
            return templates[0]
        
        # 2. Buscar por coincidencia parcial (sin grosor y acabado)
        base_name = product_name.split('-')[0].strip()
        templates = self.env['product.template'].search([
            ('is_marble_template', '=', True),
            ('name', 'ilike', base_name)
        ], limit=1)
        
        if templates:
            return templates[0]
        
        # 3. Buscar por palabras clave
        keywords = base_name.split()
        if keywords:
            domain = [('is_marble_template', '=', True)]
            for keyword in keywords:
                domain.append(('name', 'ilike', keyword))
            
            templates = self.env['product.template'].search(domain, limit=1)
            if templates:
                return templates[0]
        
        return None
    
    def action_view_created_products(self):
        """Ver productos creados desde este packing list"""
        self.ensure_one()
        created_products = self.env['product.product'].search([
            ('packing_list_import_line_id', 'in', self.line_ids.ids)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos Creados - {self.display_name}',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created_products.ids)],
            'context': {'create': False}
        }
    
    def action_cancel(self):
        """Cancelar el packing list"""
        self.ensure_one()
        if self.state == 'processed':
            raise UserError("No se puede cancelar un packing list ya procesado.")
        self.state = 'cancelled'
    
    def action_set_to_draft(self):
        """Volver a borrador"""
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
    
    # Datos del producto
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
    
    # Datos de agrupación y trazabilidad
    marble_custom_lot = fields.Char(
        string='Lote Personalizado',
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
    
    # Datos adicionales
    marble_finish = fields.Char(
        string='Acabado',
        help='Acabado del mármol extraído del nombre del producto'
    )
    
    # Datos de precio
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
    
    # Referencia al producto creado
    created_product_id = fields.Many2one(
        'product.product',
        string='Producto Creado',
        readonly=True,
        help='Producto único generado desde esta línea'
    )
    
    # Campos de estado
    is_processed = fields.Boolean(
        string='Procesado',
        compute='_compute_is_processed',
        store=True
    )
    
    # Campos de validación
    has_errors = fields.Boolean(
        string='Tiene Errores',
        default=False
    )
    
    error_message = fields.Text(
        string='Mensaje de Error'
    )
    
    @api.depends('marble_height', 'marble_width')
    def _compute_marble_sqm(self):
        """Calcular metros cuadrados"""
        for record in self:
            if record.marble_height and record.marble_width:
                record.marble_sqm = (record.marble_height * record.marble_width) / 10000
            else:
                record.marble_sqm = 0.0
    
    @api.depends('created_product_id')
    def _compute_is_processed(self):
        """Determinar si la línea ha sido procesada"""
        for record in self:
            record.is_processed = bool(record.created_product_id)
    
    @api.onchange('product_name')
    def _onchange_product_name(self):
        """Extraer información del nombre del producto"""
        if self.product_name:
            # Intentar extraer el acabado del nombre
            name_parts = self.product_name.split('-')
            if len(name_parts) > 1:
                # Buscar acabados conocidos
                finishes = ['Leather', 'Polished', 'Honed', 'Brushed', 'Antique']
                for part in name_parts:
                    if any(finish.lower() in part.lower() for finish in finishes):
                        self.marble_finish = part.strip()
                        break
    
    @api.constrains('marble_height', 'marble_width', 'marble_thickness')
    def _check_dimensions(self):
        """Validar dimensiones"""
        for record in self:
            if record.marble_height <= 0:
                raise ValidationError("El alto debe ser mayor a cero.")
            if record.marble_width <= 0:
                raise ValidationError("El ancho debe ser mayor a cero.")
            if record.marble_thickness <= 0:
                raise ValidationError("El grosor debe ser mayor a cero.")
    
    def action_view_created_product(self):
        """Ver el producto creado"""
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