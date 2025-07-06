-e ### ./data/ir_sequence_data.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Secuencia para números de serie de productos de mármol -->
        <record id="sequence_marble_product_serial" model="ir.sequence">
            <field name="name">Marble Product Serial</field>
            <field name="code">marble.product.serial</field>
            <field name="prefix">MP</field>
            <field name="padding">5</field>
            <field name="number_increment">1</field>
            <field name="number_next">1</field>
            <field name="company_id" eval="False"/>
            <field name="implementation">standard</field>
        </record>
        
        <!-- Secuencia para packing lists -->
        <record id="sequence_packing_list" model="ir.sequence">
            <field name="name">Packing List Import</field>
            <field name="code">packing.list.import</field>
            <field name="prefix">PL</field>
            <field name="padding">4</field>
            <field name="number_increment">1</field>
            <field name="number_next">1</field>
            <field name="company_id" eval="False"/>
            <field name="implementation">standard</field>
        </record>
        
    </data>
</odoo>
```

-e ### ./data/product_uom_data.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
  
        
    </data>
</odoo>
```

-e ### ./demo/product_demo.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Categorías de productos para mármol -->
        <record id="product_category_marble" model="product.category">
            <field name="name">Mármol y Piedras Naturales</field>
            <field name="parent_id" ref="product.product_category_all"/>
        </record>
        
        <record id="product_category_marble_natural" model="product.category">
            <field name="name">Mármol Natural</field>
            <field name="parent_id" ref="product_category_marble"/>
        </record>
        
        <record id="product_category_granite" model="product.category">
            <field name="name">Granito</field>
            <field name="parent_id" ref="product_category_marble"/>
        </record>
        
        <!-- Plantillas de mármol de ejemplo -->
        <record id="marble_template_carrara" model="product.template">
            <field name="name">Mármol Carrara</field>
            <field name="is_marble_template">True</field>
            <field name="type">consu</field>  <!-- ✅ CORREGIDO: usar 'consu' en lugar de 'product' -->
            <field name="categ_id" ref="product_category_marble_natural"/>
            <field name="uom_id" ref="uom.product_uom_meter"/>
            <field name="uom_po_id" ref="uom.product_uom_meter"/>
            <field name="tracking">none</field>
            <field name="marble_height">300.0</field>
            <field name="marble_width">150.0</field>
            <field name="marble_thickness">2.0</field>
            <field name="marble_category">marble</field>
            <field name="marble_origin">Italia</field>
            <field name="marble_finish">Polished</field>
            <field name="standard_price">120.00</field>
            <field name="price_per_sqm">60.00</field>
            <field name="description">
                Mármol Carrara italiano de alta calidad.
                Ideal para encimeras y revestimientos de lujo.
            </field>
        </record>
        
        <record id="marble_template_amazon" model="product.template">
            <field name="name">Amazon</field>
            <field name="is_marble_template">True</field>
            <field name="type">consu</field>  <!-- ✅ CORREGIDO: usar 'consu' en lugar de 'product' -->
            <field name="categ_id" ref="product_category_marble_natural"/>
            <field name="uom_id" ref="uom.product_uom_meter"/>
            <field name="uom_po_id" ref="uom.product_uom_meter"/>
            <field name="tracking">none</field>
            <field name="marble_height">320.0</field>
            <field name="marble_width">160.0</field>
            <field name="marble_thickness">2.0</field>
            <field name="marble_category">marble</field>
            <field name="marble_origin">Brasil</field>
            <field name="marble_finish">Leather</field>
            <field name="standard_price">150.00</field>
            <field name="price_per_sqm">75.00</field>
            <field name="description">
                Mármol Amazon con vetas características.
                Excelente para proyectos de alta gama.
            </field>
        </record>
        
        <record id="marble_template_metalicus" model="product.template">
            <field name="name">Metalicus</field>
            <field name="is_marble_template">True</field>
            <field name="type">consu</field>  <!-- ✅ CORREGIDO: usar 'consu' en lugar de 'product' -->
            <field name="categ_id" ref="product_category_marble_natural"/>
            <field name="uom_id" ref="uom.product_uom_meter"/>
            <field name="uom_po_id" ref="uom.product_uom_meter"/>
            <field name="tracking">none</field>
            <field name="marble_height">305.0</field>
            <field name="marble_width">155.0</field>
            <field name="marble_thickness">2.0</field>
            <field name="marble_category">marble</field>
            <field name="marble_origin">Brasil</field>
            <field name="marble_finish">Polished</field>
            <field name="standard_price">180.00</field>
            <field name="price_per_sqm">90.00</field>
            <field name="description">
                Mármol Metalicus con acabado metálico natural.
                Perfecto para diseños modernos y contemporáneos.
            </field>
        </record>
        
        <!-- Proveedor de ejemplo -->
        <record id="supplier_zucchi" model="res.partner">
            <field name="name">ZUCCHI LUXURY STONES</field>
            <field name="is_company">True</field>
            <field name="supplier_rank">1</field>
            <field name="customer_rank">0</field>
            <field name="country_id" ref="base.it"/>
            <field name="email">info@zucchiluxury.com</field>
            <field name="phone">+39 0585 123456</field>
            <field name="street">Via Carrara 123</field>
            <field name="city">Carrara</field>
            <field name="zip">54033</field>
            <field name="comment">
                Proveedor especializado en mármol italiano de alta calidad.
                Experiencia de más de 50 años en el sector.
            </field>
        </record>
        
    </data>
</odoo>
```

-e ### ./models/packing_list_import.py
```
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
            error_message = "Se encontraron los siguientes errores:
" + "
".join(errors)
            if created_products:
                error_message += f"

Se crearon {len(created_products)} productos exitosamente."
            raise UserError(error_message)
        
        # Si todo salió bien, marcar como procesado
        self.state = 'processed'
        self.purchase_order_id.packing_list_imported = True
        
        # Mostrar productos creados
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos Creados ({len(created_products)})',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', [p.id for p in created_products])],
            'context': {'create': False}
        }
    
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
```

-e ### ./models/product_product.py
```
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    # Campo para identificar productos generados automáticamente
    is_generated_marble_product = fields.Boolean(
        string='Producto Generado Automáticamente',
        default=False,
        help='Indica si este producto fue generado automáticamente desde una plantilla de mármol'
    )
    
    # Referencia al producto padre/plantilla
    marble_parent_template_id = fields.Many2one(
        'product.template',
        string='Plantilla Padre',
        help='Plantilla de mármol desde la cual se generó este producto',
        domain=[('is_marble_template', '=', True)]
    )
    
    # Número de serie único generado automáticamente
    marble_serial_number = fields.Char(
        string='Número de Serie',
        help='Número de serie único generado automáticamente',
        readonly=True,
        copy=False
    )
    
    # Campo para mostrar el stock actual
    current_stock = fields.Float(
        string='Stock Actual',
        compute='_compute_current_stock',
        store=True,  # <- IMPORTANTE: así Odoo calcula y guarda el valor
        help='Stock disponible actual'
    )

    @api.depends('stock_quant_ids.quantity', 'stock_move_ids.state', 'stock_move_ids.product_qty')
    def _compute_current_stock(self):
        """
        Calcular stock actual.
        El trigger depende de stock_quant_ids.quantity y también de movimientos por seguridad.
        """
        for product in self:
            # Lo más robusto es usar la suma de stock_quant
            product.current_stock = sum(product.stock_quant_ids.mapped('quantity'))

    
    # Estado del producto único
    marble_status = fields.Selection([
        ('draft', 'Borrador'),
        ('available', 'Disponible'),
        ('reserved', 'Reservado'),
        ('sold', 'Vendido'),
        ('damaged', 'Dañado'),
        ('archived', 'Archivado')
    ], string='Estado de la Placa', default='draft')
    
    # Fecha de creación del producto único
    marble_creation_date = fields.Datetime(
        string='Fecha de Creación',
        default=fields.Datetime.now,
        help='Fecha en que se creó este producto único'
    )
    
    # ============================================
    # CAMPOS ESPECÍFICOS PARA PRODUCTOS ÚNICOS
    # (No están en product.template)
    # ============================================
    
    # Datos específicos del packing list origen
    packing_list_import_line_id = fields.Many2one(
        'packing.list.import.line',
        string='Línea de Packing List',
        help='Línea del packing list que originó este producto'
    )
    
    # Datos de trazabilidad específicos de la placa individual
    container_number = fields.Char(
        string='Número de Contenedor',
        help='Número del contenedor específico de esta placa'
    )
    
    commercial_invoice = fields.Char(
        string='Factura Comercial',
        help='Número de factura comercial específica de esta placa'
    )
    
    supplier_lot_number = fields.Char(
        string='Número de Lote del Proveedor',
        help='Número de lote específico del proveedor para esta placa'
    )
    
    wooden_crate_code = fields.Char(
        string='Código de Atado/Bloque',
        help='Código específico del wooden crate de esta placa'
    )
    
    marble_custom_lot = fields.Char(
        string='Lote Personalizado',
        help='Lote personalizado específico de esta placa'
    )
    
    # ============================================
    # CAMPOS COMPUTADOS Y RELACIONADOS
    # ============================================
    
    # Acceso a campos del template (para facilitar búsquedas)
    marble_height = fields.Float(
        string='Alto (cm)',
        related='product_tmpl_id.marble_height',
        store=True,
        readonly=True
    )
    
    marble_width = fields.Float(
        string='Ancho (cm)',
        related='product_tmpl_id.marble_width',
        store=True,
        readonly=True
    )
    
    marble_thickness = fields.Float(
        string='Grosor (cm)',
        related='product_tmpl_id.marble_thickness',
        store=True,
        readonly=True
    )
    
    marble_sqm = fields.Float(
        string='Metros Cuadrados',
        related='product_tmpl_id.marble_sqm',
        store=True,
        readonly=True
    )
    
    marble_finish = fields.Char(
        string='Acabado',
        related='product_tmpl_id.marble_finish',
        store=True,
        readonly=True
    )
    
    marble_origin = fields.Char(
        string='Origen',
        related='product_tmpl_id.marble_origin',
        store=True,
        readonly=True
    )
    
    marble_category = fields.Selection(
        string='Categoría de Piedra',
        related='product_tmpl_id.marble_category',
        store=True,
        readonly=True
    )
    
    price_per_sqm = fields.Float(
        string='Precio por M²',
        related='product_tmpl_id.price_per_sqm',
        store=True,
        readonly=True
    )
    
    @api.depends('stock_quant_ids.quantity')
    def _compute_current_stock(self):
        """Calcular stock actual"""
        for product in self:
            product.current_stock = sum(product.stock_quant_ids.mapped('quantity'))
    
    @api.model
    def create_marble_product_from_template(self, template_id, marble_data, packing_line_id=None):
        """
        Crear un producto único de mármol basado en una plantilla
        
        Args:
            template_id (int): ID de la plantilla de mármol
            marble_data (dict): Datos específicos de la placa
            packing_line_id (int): ID de la línea del packing list
            
        Returns:
            product.product: Producto creado
        """
        template = self.env['product.template'].browse(template_id)
        
        if not template.exists():
            raise ValidationError(_("La plantilla especificada no existe."))
            
        if not template.is_marble_template:
            raise ValidationError(_("El producto seleccionado no es una plantilla de mármol."))
        
        # Generar número de serie único
        serial_number = self._generate_marble_serial_number(
            marble_data.get('marble_custom_lot', ''),
            marble_data.get('supplier_lot_number', '')
        )
        
        # Crear nombre único del producto
        product_name = self._generate_marble_product_name(template, marble_data, serial_number)
        
        # ============================================
        # ACTUALIZAR CAMPOS DEL TEMPLATE CON DATOS ESPECÍFICOS
        # ============================================
        
        # Actualizar template con datos específicos de esta placa
        template.write({
            'marble_height': marble_data.get('marble_height', template.marble_height),
            'marble_width': marble_data.get('marble_width', template.marble_width),
            'marble_thickness': marble_data.get('marble_thickness', template.marble_thickness),
            'marble_finish': marble_data.get('marble_finish', template.marble_finish) or template.marble_finish,
        })
        
        # Preparar valores para el nuevo producto
        product_vals = {
            'name': product_name,
            'product_tmpl_id': template.id,
            'is_generated_marble_product': True,
            'marble_parent_template_id': template.id,
            'marble_serial_number': serial_number,
            'marble_status': 'draft',
            'marble_creation_date': fields.Datetime.now(),
            
            # Configuración del producto
            'type': 'consu',
            'tracking': 'serial',
            'categ_id': template.categ_id.id,
            
            # ============================================
            # SOLO CAMPOS ESPECÍFICOS DEL PRODUCTO ÚNICO
            # ============================================
            'marble_custom_lot': marble_data.get('marble_custom_lot', ''),
            'wooden_crate_code': marble_data.get('wooden_crate_code', ''),
            'container_number': marble_data.get('container_number', ''),
            'commercial_invoice': marble_data.get('commercial_invoice', ''),
            'supplier_lot_number': marble_data.get('supplier_lot_number', ''),
            
            # Datos de precio específicos
            'standard_price': marble_data.get('cost_price', template.standard_price),
            
            # Referencia al packing list
            'packing_list_import_line_id': packing_line_id,
        }
        
        # Crear el producto
        product = self.create(product_vals)
        
        # Crear el número de serie (stock.lot)
        lot_vals = {
            'name': serial_number,
            'product_id': product.id,
            'company_id': self.env.company.id,
        }
        lot = self.env['stock.lot'].create(lot_vals)
        
        _logger.info(f"Producto de mármol creado: {product.name} (ID: {product.id}) con lote: {lot.name}")
        
        return product
    
    def _generate_marble_serial_number(self, custom_lot, supplier_lot):
        """
        Generar un número de serie único basado en el lote personalizado
        
        Args:
            custom_lot (str): Lote personalizado/wooden crate
            supplier_lot (str): Número de lote del proveedor
            
        Returns:
            str: Número de serie único
        """
        # Obtener secuencia base
        sequence = self.env['ir.sequence'].next_by_code('marble.product.serial')
        
        if not sequence:
            # Fallback si la secuencia no existe
            sequence = self.env['ir.sequence'].sudo().create({
                'name': 'Marble Product Serial',
                'code': 'marble.product.serial',
                'prefix': 'MP',
                'padding': 5,
                'number_increment': 1,
                'number_next': 1,
            }).next_by_code('marble.product.serial')
        
        if custom_lot and supplier_lot:
            # Formato: LOTE_PERSONALIZADO-LOTE_PROVEEDOR-SECUENCIA
            return f"{custom_lot}-{supplier_lot}-{sequence}"
        elif custom_lot:
            # Formato: LOTE_PERSONALIZADO-SECUENCIA  
            return f"{custom_lot}-{sequence}"
        elif supplier_lot:
            # Formato: LOTE_PROVEEDOR-SECUENCIA
            return f"{supplier_lot}-{sequence}"
        else:
            # Solo secuencia
            return f"MP-{sequence}"
    
    def _generate_marble_product_name(self, template, marble_data, serial_number):
        """
        Generar el nombre del producto basado en la plantilla y los datos
        
        Args:
            template (product.template): Plantilla base
            marble_data (dict): Datos específicos de la placa
            serial_number (str): Número de serie generado
            
        Returns:
            str: Nombre del producto
        """
        base_name = template.name
        height = marble_data.get('marble_height', 0)
        width = marble_data.get('marble_width', 0)
        thickness = marble_data.get('marble_thickness', template.marble_thickness)
        finish = marble_data.get('marble_finish', template.marble_finish)
        
        # Construir nombre: "Nombre Base - Grosor - Acabado - Dimensiones - Serial"
        name_parts = [base_name]
        
        if thickness:
            name_parts.append(f"{thickness}cm")
            
        if finish:
            name_parts.append(finish)
        
        if height and width:
            name_parts.append(f"{height:.0f}x{width:.0f}")
        
        name_parts.append(serial_number)
        
        return " - ".join(name_parts)
    
    def action_set_available(self):
        """Marcar la placa como disponible"""
        self.ensure_one()
        if self.marble_status == 'draft':
            self.marble_status = 'available'
            _logger.info(f"Producto de mármol marcado como disponible: {self.name}")
    
    def action_set_sold(self):
        """Marcar la placa como vendida"""
        self.ensure_one()
        if self.marble_status in ['available', 'reserved']:
            self.marble_status = 'sold'
            _logger.info(f"Producto de mármol marcado como vendido: {self.name}")
    
    def action_set_damaged(self):
        """Marcar la placa como dañada"""
        self.ensure_one()
        self.marble_status = 'damaged'
        _logger.info(f"Producto de mármol marcado como dañado: {self.name}")
    
    def action_archive_marble_product(self):
        """Archivar el producto de mármol"""
        self.ensure_one()
        self.marble_status = 'archived'
        self.active = False
        _logger.info(f"Producto de mármol archivado: {self.name}")
    
    def action_view_stock_moves(self):
        """Ver movimientos de stock de este producto"""
        self.ensure_one()
        moves = self.env['stock.move'].search([
            ('product_id', '=', self.id)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Movimientos - %s') % self.name,
            'res_model': 'stock.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', moves.ids)],
            'context': {'create': False}
        }
    
    def action_view_packing_list(self):
        """Ver el packing list origen"""
        self.ensure_one()
        if self.packing_list_import_line_id:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Packing List Origen'),
                'res_model': 'packing.list.import',
                'res_id': self.packing_list_import_line_id.packing_list_id.id,
                'view_mode': 'form',
                'target': 'current'
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _('Este producto no tiene packing list asociado'),
                    'type': 'warning',
                }
            }
    
    @api.model
    def auto_archive_zero_stock_products(self):
        """
        Método para archivar automáticamente productos con stock cero
        Se puede ejecutar como cron job
        """
        products_to_archive = self.search([
            ('is_generated_marble_product', '=', True),
            ('active', '=', True),
            ('marble_status', 'in', ['available', 'sold']),
        ])
        
        archived_count = 0
        for product in products_to_archive:
            if product.current_stock <= 0:
                product.action_archive_marble_product()
                archived_count += 1
        
        _logger.info(f"Archivados automáticamente {archived_count} productos de mármol con stock cero")
        return archived_count
    
    def write(self, vals):
        """Sobrescribir write para validaciones específicas de mármol"""
        # Validar que no se pueda cambiar el estado si está vendido
        if 'marble_status' in vals and vals['marble_status'] != 'sold':
            for product in self:
                if product.marble_status == 'sold' and product.is_generated_marble_product:
                    raise ValidationError(_("No se puede cambiar el estado de un producto vendido."))
        
        return super().write(vals)
    
    @api.constrains('marble_status', 'current_stock')
    def _check_marble_status_stock(self):
        """Validar coherencia entre estado y stock"""
        for product in self:
            if product.is_generated_marble_product:
                if product.marble_status == 'sold' and product.current_stock > 0:
                    raise ValidationError(
                        _("Un producto vendido no puede tener stock positivo: %s") % product.name
                    )
                if product.marble_status == 'available' and product.current_stock <= 0:
                    _logger.warning(
                        f"Producto disponible sin stock: {product.name} "
                        f"(Stock: {product.current_stock})"
                    )
```

-e ### ./models/product_template.py
```
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Campo identificador de plantilla de mármol
    is_marble_template = fields.Boolean(
        string='Es Plantilla de Mármol',
        default=False,
        help='Indica si este producto es una plantilla base para crear productos únicos de mármol'
    )
    
    # Campos específicos del mármol - Dimensiones
    marble_height = fields.Float(
        string='Alto (cm)',
        digits=(10, 2),
        help='Alto de la placa en centímetros'
    )
    
    marble_width = fields.Float(
        string='Ancho (cm)', 
        digits=(10, 2),
        help='Ancho de la placa en centímetros'
    )
    
    marble_thickness = fields.Float(
        string='Grosor (cm)',
        digits=(10, 2),
        help='Grosor de la placa en centímetros'
    )
    
    marble_sqm = fields.Float(
        string='Metros Cuadrados',
        compute='_compute_marble_sqm',
        store=True,
        digits=(10, 4),
        help='Metros cuadrados calculados automáticamente (Alto x Ancho / 10000)'
    )
    
    # Campos de precio
    price_per_sqm = fields.Float(
        string='Precio por M²',
        digits='Product Price',
        help='Precio por metro cuadrado para cálculos automáticos'
    )
    
    # Campos adicionales para el flujo de negocio
    marble_finish = fields.Char(
        string='Acabado',
        help='Tipo de acabado (Pulido, Leather, Antique, etc.)'
    )
    
    marble_origin = fields.Char(
        string='Origen',
        help='País o región de origen del mármol'
    )
    
    marble_category = fields.Selection([
        ('marble', 'Mármol'),
        ('granite', 'Granito'),
        ('quartzite', 'Cuarcita'),
        ('limestone', 'Piedra Caliza'),
        ('travertine', 'Travertino'),
        ('onyx', 'Ónix'),
        ('other', 'Otro')
    ], string='Categoría de Piedra', default='marble')
    
    # Campo computado para contar productos generados
    generated_products_count = fields.Integer(
        string='Productos Generados',
        compute='_compute_generated_products_count',
        help='Número de productos únicos generados desde esta plantilla'
    )
    
    @api.depends('marble_height', 'marble_width')
    def _compute_marble_sqm(self):
        """Calcular metros cuadrados basado en alto y ancho"""
        for record in self:
            if record.marble_height and record.marble_width:
                # Convertir de cm² a m² (dividir por 10000)
                record.marble_sqm = (record.marble_height * record.marble_width) / 10000
            else:
                record.marble_sqm = 0.0
    
    def _compute_generated_products_count(self):
        """Calcular número de productos generados"""
        for record in self:
            if record.is_marble_template:
                generated_products = self.env['product.product'].search_count([
                    ('marble_parent_template_id', '=', record.id)
                ])
                record.generated_products_count = generated_products
            else:
                record.generated_products_count = 0
    
    @api.onchange('is_marble_template')
    def _onchange_is_marble_template(self):
        """Configurar valores por defecto para plantillas de mármol"""
        if self.is_marble_template:
            # ✅ CORRECCIÓN: Usar 'consu' (Bienes) en lugar de 'product' según la imagen.
            # 'product' (Producto Almacenable) no está disponible en tu entorno.
            self.type = 'consu'
            self.tracking = 'none'  # Las plantillas no se trackean
            
            # Buscar UoM correcta sin crear duplicados
            try:
                # 1. Intentar usar la referencia estándar de Odoo
                sqm_uom = self.env.ref('uom.product_uom_square_meter', raise_if_not_found=False)
                
                if not sqm_uom:
                    # 2. Buscar por nombre en la categoría Surface
                    surface_category = self.env.ref('uom.uom_categ_surface', raise_if_not_found=False)
                    if surface_category:
                        sqm_uom = self.env['uom.uom'].search([
                            ('category_id', '=', surface_category.id),
                            ('uom_type', '=', 'reference')
                        ], limit=1)
                
                if not sqm_uom:
                    # 3. Buscar cualquier UoM de superficie como referencia
                    sqm_uom = self.env['uom.uom'].search([
                        ('name', 'in', ['m²', 'Square Meter', 'Metro Cuadrado', 'Square Metres'])
                    ], limit=1)
                
                if sqm_uom:
                    self.uom_id = sqm_uom.id
                    self.uom_po_id = sqm_uom.id
                else:
                    # 4. Fallback: usar metros lineales
                    meter_uom = self.env.ref('uom.product_uom_meter', raise_if_not_found=False)
                    if meter_uom:
                        self.uom_id = meter_uom.id
                        self.uom_po_id = meter_uom.id
                    
            except Exception as e:
                # Si hay cualquier error, usar metros lineales como fallback seguro
                meter_uom = self.env.ref('uom.product_uom_meter', raise_if_not_found=False)
                if meter_uom:
                    self.uom_id = meter_uom.id
                    self.uom_po_id = meter_uom.id
    
    @api.constrains('marble_height', 'marble_width', 'marble_thickness')
    def _check_marble_dimensions(self):
        """Validar que las dimensiones sean positivas"""
        for record in self:
            if record.is_marble_template:
                if record.marble_height and record.marble_height <= 0:
                    raise ValidationError(_("El alto debe ser mayor a cero."))
                if record.marble_width and record.marble_width <= 0:
                    raise ValidationError(_("El ancho debe ser mayor a cero."))
                if record.marble_thickness and record.marble_thickness <= 0:
                    raise ValidationError(_("El grosor debe ser mayor a cero."))
    
    @api.constrains('is_marble_template', 'marble_sqm')
    def _check_marble_template_sqm(self):
        """Validar que las plantillas de mármol tengan metros cuadrados"""
        for record in self:
            if record.is_marble_template and not record.marble_sqm:
                raise ValidationError(_(
                    "Las plantillas de mármol deben tener dimensiones válidas para calcular los metros cuadrados."
                ))
    
    def name_get(self):
        """Personalizar el nombre mostrado para plantillas de mármol"""
        result = []
        for record in self:
            name = record.name
            if record.is_marble_template:
                name_parts = [name]
                
                if record.marble_thickness:
                    name_parts.append(f"{record.marble_thickness}cm")
                    
                if record.marble_finish:
                    name_parts.append(record.marble_finish)
                
                if record.marble_origin:
                    name_parts.append(f"({record.marble_origin})")
                
                name = " - ".join(name_parts)
            
            result.append((record.id, name))
        return result
    
    def action_view_generated_products(self):
        """Ver productos generados desde esta plantilla"""
        self.ensure_one()
        generated_products = self.env['product.product'].search([
            ('marble_parent_template_id', '=', self.id)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Productos Generados - %s') % self.name,
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', generated_products.ids)],
            'context': {
                'create': False,
                'default_marble_parent_template_id': self.id,
                'search_default_marble_products': 1,
            }
        }
    
    def action_create_marble_variant(self):
        """Crear variante manual de mármol para casos especiales"""
        self.ensure_one()
        
        if not self.is_marble_template:
            raise ValidationError(_("Solo se pueden crear variantes desde plantillas de mármol."))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Crear Variante de Mármol'),
            'res_model': 'product.product',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_tmpl_id': self.id,
                'default_is_generated_marble_product': True,
                'default_marble_parent_template_id': self.id,
                'default_marble_status': 'draft',
                'form_view_initial_mode': 'edit',
            }
        }
    
    def action_duplicate_as_template(self):
        """Duplicar como nueva plantilla de mármol"""
        self.ensure_one()
        
        copy_vals = {
            'name': _('%s (Copia)') % self.name,
            'is_marble_template': True,
        }
        
        new_template = self.copy(copy_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Nueva Plantilla de Mármol'),
            'res_model': 'product.template',
            'res_id': new_template.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def write(self, vals):
        """Sobrescribir write para validaciones y actualizaciones automáticas"""
        # Si se cambian las dimensiones, recalcular m²
        if any(field in vals for field in ['marble_height', 'marble_width']):
            for record in self:
                if record.is_marble_template:
                    # Forzar recálculo después del write
                    result = super(ProductTemplate, record).write(vals)
                    record._compute_marble_sqm()
                    return result
        
        return super().write(vals)
    
    @api.model
    def create(self, vals):
        """Sobrescribir create para configuraciones automáticas"""
        # Si es plantilla de mármol, asegurar configuraciones
        if vals.get('is_marble_template'):
            # ✅ CORRECCIÓN: Usar 'consu' (Bienes) en lugar de 'product' según la imagen.
            vals.setdefault('type', 'consu')
            vals.setdefault('tracking', 'none')
            
            # Configurar UoM de manera segura
            if 'uom_id' not in vals or 'uom_po_id' not in vals:
                # Buscar UoM de superficie existente
                sqm_uom = self.env.ref('uom.product_uom_square_meter', raise_if_not_found=False)
                if not sqm_uom:
                    # Buscar en categoría Surface
                    surface_category = self.env.ref('uom.uom_categ_surface', raise_if_not_found=False)
                    if surface_category:
                        sqm_uom = self.env['uom.uom'].search([
                            ('category_id', '=', surface_category.id),
                            ('uom_type', '=', 'reference')
                        ], limit=1)
                
                if sqm_uom:
                    vals.setdefault('uom_id', sqm_uom.id)
                    vals.setdefault('uom_po_id', sqm_uom.id)
                else:
                    # Fallback seguro: metros lineales
                    meter_uom = self.env.ref('uom.product_uom_meter', raise_if_not_found=False)
                    if meter_uom:
                        vals.setdefault('uom_id', meter_uom.id)
                        vals.setdefault('uom_po_id', meter_uom.id)
        
        return super().create(vals)
    
    @api.model
    def search_marble_templates_by_name(self, name_pattern):
        """Búsqueda especializada para plantillas de mármol por nombre"""
        domain = [
            ('is_marble_template', '=', True),
            '|', '|', '|',
            ('name', 'ilike', name_pattern),
            ('marble_finish', 'ilike', name_pattern),
            ('marble_origin', 'ilike', name_pattern),
            ('marble_category', 'ilike', name_pattern),
        ]
        
        return self.search(domain)
    
    def get_marble_info_summary(self):
        """Obtener resumen de información de mármol para reportes"""
        self.ensure_one()
        
        if not self.is_marble_template:
            return {}
        
        return {
            'name': self.name,
            'dimensions': f"{self.marble_height} x {self.marble_width} x {self.marble_thickness} cm",
            'sqm': self.marble_sqm,
            'category': dict(self._fields['marble_category'].selection).get(self.marble_category),
            'origin': self.marble_origin or _('No especificado'),
            'finish': self.marble_finish or _('No especificado'),
            'price_per_sqm': self.price_per_sqm,
            'generated_products': self.generated_products_count,
        }
```

-e ### ./models/purchase_order_line.py
```
from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_marble_template = fields.Boolean(
        string='¿Es Mármol?',
        related='product_id.is_marble_template',
        store=True,
        readonly=True
    )
```

-e ### ./models/purchase_order.py
```
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
```

-e ### ./models/stock_picking.py
```
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
```

-e ### ./salida_modulo_completo.md
```
-e ### ./data/ir_sequence_data.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Secuencia para números de serie de productos de mármol -->
        <record id="sequence_marble_product_serial" model="ir.sequence">
            <field name="name">Marble Product Serial</field>
            <field name="code">marble.product.serial</field>
            <field name="prefix">MP</field>
            <field name="padding">5</field>
            <field name="number_increment">1</field>
            <field name="number_next">1</field>
            <field name="company_id" eval="False"/>
            <field name="implementation">standard</field>
        </record>
        
        <!-- Secuencia para packing lists -->
        <record id="sequence_packing_list" model="ir.sequence">
            <field name="name">Packing List Import</field>
            <field name="code">packing.list.import</field>
            <field name="prefix">PL</field>
            <field name="padding">4</field>
            <field name="number_increment">1</field>
            <field name="number_next">1</field>
            <field name="company_id" eval="False"/>
            <field name="implementation">standard</field>
        </record>
        
    </data>
</odoo>
```

-e ### ./data/product_uom_data.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
  
        
    </data>
</odoo>
```

-e ### ./demo/product_demo.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Categorías de productos para mármol -->
        <record id="product_category_marble" model="product.category">
            <field name="name">Mármol y Piedras Naturales</field>
            <field name="parent_id" ref="product.product_category_all"/>
        </record>
        
        <record id="product_category_marble_natural" model="product.category">
            <field name="name">Mármol Natural</field>
            <field name="parent_id" ref="product_category_marble"/>
        </record>
        
        <record id="product_category_granite" model="product.category">
            <field name="name">Granito</field>
            <field name="parent_id" ref="product_category_marble"/>
        </record>
        
        <!-- Plantillas de mármol de ejemplo -->
        <record id="marble_template_carrara" model="product.template">
            <field name="name">Mármol Carrara</field>
            <field name="is_marble_template">True</field>
            <field name="type">consu</field>  <!-- ✅ CORREGIDO: usar 'consu' en lugar de 'product' -->
            <field name="categ_id" ref="product_category_marble_natural"/>
            <field name="uom_id" ref="uom.product_uom_meter"/>
            <field name="uom_po_id" ref="uom.product_uom_meter"/>
            <field name="tracking">none</field>
            <field name="marble_height">300.0</field>
            <field name="marble_width">150.0</field>
            <field name="marble_thickness">2.0</field>
            <field name="marble_category">marble</field>
            <field name="marble_origin">Italia</field>
            <field name="marble_finish">Polished</field>
            <field name="standard_price">120.00</field>
            <field name="price_per_sqm">60.00</field>
            <field name="description">
                Mármol Carrara italiano de alta calidad.
                Ideal para encimeras y revestimientos de lujo.
            </field>
        </record>
        
        <record id="marble_template_amazon" model="product.template">
            <field name="name">Amazon</field>
            <field name="is_marble_template">True</field>
            <field name="type">consu</field>  <!-- ✅ CORREGIDO: usar 'consu' en lugar de 'product' -->
            <field name="categ_id" ref="product_category_marble_natural"/>
            <field name="uom_id" ref="uom.product_uom_meter"/>
            <field name="uom_po_id" ref="uom.product_uom_meter"/>
            <field name="tracking">none</field>
            <field name="marble_height">320.0</field>
            <field name="marble_width">160.0</field>
            <field name="marble_thickness">2.0</field>
            <field name="marble_category">marble</field>
            <field name="marble_origin">Brasil</field>
            <field name="marble_finish">Leather</field>
            <field name="standard_price">150.00</field>
            <field name="price_per_sqm">75.00</field>
            <field name="description">
                Mármol Amazon con vetas características.
                Excelente para proyectos de alta gama.
            </field>
        </record>
        
        <record id="marble_template_metalicus" model="product.template">
            <field name="name">Metalicus</field>
            <field name="is_marble_template">True</field>
            <field name="type">consu</field>  <!-- ✅ CORREGIDO: usar 'consu' en lugar de 'product' -->
            <field name="categ_id" ref="product_category_marble_natural"/>
            <field name="uom_id" ref="uom.product_uom_meter"/>
            <field name="uom_po_id" ref="uom.product_uom_meter"/>
            <field name="tracking">none</field>
            <field name="marble_height">305.0</field>
            <field name="marble_width">155.0</field>
            <field name="marble_thickness">2.0</field>
            <field name="marble_category">marble</field>
            <field name="marble_origin">Brasil</field>
            <field name="marble_finish">Polished</field>
            <field name="standard_price">180.00</field>
            <field name="price_per_sqm">90.00</field>
            <field name="description">
                Mármol Metalicus con acabado metálico natural.
                Perfecto para diseños modernos y contemporáneos.
            </field>
        </record>
        
        <!-- Proveedor de ejemplo -->
        <record id="supplier_zucchi" model="res.partner">
            <field name="name">ZUCCHI LUXURY STONES</field>
            <field name="is_company">True</field>
            <field name="supplier_rank">1</field>
            <field name="customer_rank">0</field>
            <field name="country_id" ref="base.it"/>
            <field name="email">info@zucchiluxury.com</field>
            <field name="phone">+39 0585 123456</field>
            <field name="street">Via Carrara 123</field>
            <field name="city">Carrara</field>
            <field name="zip">54033</field>
            <field name="comment">
                Proveedor especializado en mármol italiano de alta calidad.
                Experiencia de más de 50 años en el sector.
            </field>
        </record>
        
    </data>
</odoo>
```

-e ### ./models/packing_list_import.py
```
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
            error_message = "Se encontraron los siguientes errores:
" + "
".join(errors)
            if created_products:
                error_message += f"

Se crearon {len(created_products)} productos exitosamente."
            raise UserError(error_message)
        
        # Si todo salió bien, marcar como procesado
        self.state = 'processed'
        self.purchase_order_id.packing_list_imported = True
        
        # Mostrar productos creados
        return {
            'type': 'ir.actions.act_window',
            'name': f'Productos Creados ({len(created_products)})',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', [p.id for p in created_products])],
            'context': {'create': False}
        }
    
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
```

-e ### ./models/product_product.py
```
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    # Campo para identificar productos generados automáticamente
    is_generated_marble_product = fields.Boolean(
        string='Producto Generado Automáticamente',
        default=False,
        help='Indica si este producto fue generado automáticamente desde una plantilla de mármol'
    )
    
    # Referencia al producto padre/plantilla
    marble_parent_template_id = fields.Many2one(
        'product.template',
        string='Plantilla Padre',
        help='Plantilla de mármol desde la cual se generó este producto',
        domain=[('is_marble_template', '=', True)]
    )
    
    # Número de serie único generado automáticamente
    marble_serial_number = fields.Char(
        string='Número de Serie',
        help='Número de serie único generado automáticamente',
        readonly=True,
        copy=False
    )
    
    # Campo para mostrar el stock actual
    current_stock = fields.Float(
        string='Stock Actual',
        compute='_compute_current_stock',
        store=True,  # <- IMPORTANTE: así Odoo calcula y guarda el valor
        help='Stock disponible actual'
    )

    @api.depends('stock_quant_ids.quantity', 'stock_move_ids.state', 'stock_move_ids.product_qty')
    def _compute_current_stock(self):
        """
        Calcular stock actual.
        El trigger depende de stock_quant_ids.quantity y también de movimientos por seguridad.
        """
        for product in self:
            # Lo más robusto es usar la suma de stock_quant
            product.current_stock = sum(product.stock_quant_ids.mapped('quantity'))

    
    # Estado del producto único
    marble_status = fields.Selection([
        ('draft', 'Borrador'),
        ('available', 'Disponible'),
        ('reserved', 'Reservado'),
        ('sold', 'Vendido'),
        ('damaged', 'Dañado'),
        ('archived', 'Archivado')
    ], string='Estado de la Placa', default='draft')
    
    # Fecha de creación del producto único
    marble_creation_date = fields.Datetime(
        string='Fecha de Creación',
        default=fields.Datetime.now,
        help='Fecha en que se creó este producto único'
    )
    
    # ============================================
    # CAMPOS ESPECÍFICOS PARA PRODUCTOS ÚNICOS
    # (No están en product.template)
    # ============================================
    
    # Datos específicos del packing list origen
    packing_list_import_line_id = fields.Many2one(
        'packing.list.import.line',
        string='Línea de Packing List',
        help='Línea del packing list que originó este producto'
    )
    
    # Datos de trazabilidad específicos de la placa individual
    container_number = fields.Char(
        string='Número de Contenedor',
        help='Número del contenedor específico de esta placa'
    )
    
    commercial_invoice = fields.Char(
        string='Factura Comercial',
        help='Número de factura comercial específica de esta placa'
    )
    
    supplier_lot_number = fields.Char(
        string='Número de Lote del Proveedor',
        help='Número de lote específico del proveedor para esta placa'
    )
    
    wooden_crate_code = fields.Char(
        string='Código de Atado/Bloque',
        help='Código específico del wooden crate de esta placa'
    )
    
    marble_custom_lot = fields.Char(
        string='Lote Personalizado',
        help='Lote personalizado específico de esta placa'
    )
    
    # ============================================
    # CAMPOS COMPUTADOS Y RELACIONADOS
    # ============================================
    
    # Acceso a campos del template (para facilitar búsquedas)
    marble_height = fields.Float(
        string='Alto (cm)',
        related='product_tmpl_id.marble_height',
        store=True,
        readonly=True
    )
    
    marble_width = fields.Float(
        string='Ancho (cm)',
        related='product_tmpl_id.marble_width',
        store=True,
        readonly=True
    )
    
    marble_thickness = fields.Float(
        string='Grosor (cm)',
        related='product_tmpl_id.marble_thickness',
        store=True,
        readonly=True
    )
    
    marble_sqm = fields.Float(
        string='Metros Cuadrados',
        related='product_tmpl_id.marble_sqm',
        store=True,
        readonly=True
    )
    
    marble_finish = fields.Char(
        string='Acabado',
        related='product_tmpl_id.marble_finish',
        store=True,
        readonly=True
    )
    
    marble_origin = fields.Char(
        string='Origen',
        related='product_tmpl_id.marble_origin',
        store=True,
        readonly=True
    )
    
    marble_category = fields.Selection(
        string='Categoría de Piedra',
        related='product_tmpl_id.marble_category',
        store=True,
        readonly=True
    )
    
    price_per_sqm = fields.Float(
        string='Precio por M²',
        related='product_tmpl_id.price_per_sqm',
        store=True,
        readonly=True
    )
    
    @api.depends('stock_quant_ids.quantity')
    def _compute_current_stock(self):
        """Calcular stock actual"""
        for product in self:
            product.current_stock = sum(product.stock_quant_ids.mapped('quantity'))
    
    @api.model
    def create_marble_product_from_template(self, template_id, marble_data, packing_line_id=None):
        """
        Crear un producto único de mármol basado en una plantilla
        
        Args:
            template_id (int): ID de la plantilla de mármol
            marble_data (dict): Datos específicos de la placa
            packing_line_id (int): ID de la línea del packing list
            
        Returns:
            product.product: Producto creado
        """
        template = self.env['product.template'].browse(template_id)
        
        if not template.exists():
            raise ValidationError(_("La plantilla especificada no existe."))
            
        if not template.is_marble_template:
            raise ValidationError(_("El producto seleccionado no es una plantilla de mármol."))
        
        # Generar número de serie único
        serial_number = self._generate_marble_serial_number(
            marble_data.get('marble_custom_lot', ''),
            marble_data.get('supplier_lot_number', '')
        )
        
        # Crear nombre único del producto
        product_name = self._generate_marble_product_name(template, marble_data, serial_number)
        
        # ============================================
        # ACTUALIZAR CAMPOS DEL TEMPLATE CON DATOS ESPECÍFICOS
        # ============================================
        
        # Actualizar template con datos específicos de esta placa
        template.write({
            'marble_height': marble_data.get('marble_height', template.marble_height),
            'marble_width': marble_data.get('marble_width', template.marble_width),
            'marble_thickness': marble_data.get('marble_thickness', template.marble_thickness),
            'marble_finish': marble_data.get('marble_finish', template.marble_finish) or template.marble_finish,
        })
        
        # Preparar valores para el nuevo producto
        product_vals = {
            'name': product_name,
            'product_tmpl_id': template.id,
            'is_generated_marble_product': True,
            'marble_parent_template_id': template.id,
            'marble_serial_number': serial_number,
            'marble_status': 'draft',
            'marble_creation_date': fields.Datetime.now(),
            
            # Configuración del producto
            'type': 'consu',
            'tracking': 'serial',
            'categ_id': template.categ_id.id,
            
            # ============================================
            # SOLO CAMPOS ESPECÍFICOS DEL PRODUCTO ÚNICO
            # ============================================
            'marble_custom_lot': marble_data.get('marble_custom_lot', ''),
            'wooden_crate_code': marble_data.get('wooden_crate_code', ''),
            'container_number': marble_data.get('container_number', ''),
            'commercial_invoice': marble_data.get('commercial_invoice', ''),
            'supplier_lot_number': marble_data.get('supplier_lot_number', ''),
            
            # Datos de precio específicos
            'standard_price': marble_data.get('cost_price', template.standard_price),
            
            # Referencia al packing list
            'packing_list_import_line_id': packing_line_id,
        }
        
        # Crear el producto
        product = self.create(product_vals)
        
        # Crear el número de serie (stock.lot)
        lot_vals = {
            'name': serial_number,
            'product_id': product.id,
            'company_id': self.env.company.id,
        }
        lot = self.env['stock.lot'].create(lot_vals)
        
        _logger.info(f"Producto de mármol creado: {product.name} (ID: {product.id}) con lote: {lot.name}")
        
        return product
    
    def _generate_marble_serial_number(self, custom_lot, supplier_lot):
        """
        Generar un número de serie único basado en el lote personalizado
        
        Args:
            custom_lot (str): Lote personalizado/wooden crate
            supplier_lot (str): Número de lote del proveedor
            
        Returns:
            str: Número de serie único
        """
        # Obtener secuencia base
        sequence = self.env['ir.sequence'].next_by_code('marble.product.serial')
        
        if not sequence:
            # Fallback si la secuencia no existe
            sequence = self.env['ir.sequence'].sudo().create({
                'name': 'Marble Product Serial',
                'code': 'marble.product.serial',
                'prefix': 'MP',
                'padding': 5,
                'number_increment': 1,
                'number_next': 1,
            }).next_by_code('marble.product.serial')
        
        if custom_lot and supplier_lot:
            # Formato: LOTE_PERSONALIZADO-LOTE_PROVEEDOR-SECUENCIA
            return f"{custom_lot}-{supplier_lot}-{sequence}"
        elif custom_lot:
            # Formato: LOTE_PERSONALIZADO-SECUENCIA  
            return f"{custom_lot}-{sequence}"
        elif supplier_lot:
            # Formato: LOTE_PROVEEDOR-SECUENCIA
            return f"{supplier_lot}-{sequence}"
        else:
            # Solo secuencia
            return f"MP-{sequence}"
    
    def _generate_marble_product_name(self, template, marble_data, serial_number):
        """
        Generar el nombre del producto basado en la plantilla y los datos
        
        Args:
            template (product.template): Plantilla base
            marble_data (dict): Datos específicos de la placa
            serial_number (str): Número de serie generado
            
        Returns:
            str: Nombre del producto
        """
        base_name = template.name
        height = marble_data.get('marble_height', 0)
        width = marble_data.get('marble_width', 0)
        thickness = marble_data.get('marble_thickness', template.marble_thickness)
        finish = marble_data.get('marble_finish', template.marble_finish)
        
        # Construir nombre: "Nombre Base - Grosor - Acabado - Dimensiones - Serial"
        name_parts = [base_name]
        
        if thickness:
            name_parts.append(f"{thickness}cm")
            
        if finish:
            name_parts.append(finish)
        
        if height and width:
            name_parts.append(f"{height:.0f}x{width:.0f}")
        
        name_parts.append(serial_number)
        
        return " - ".join(name_parts)
    
    def action_set_available(self):
        """Marcar la placa como disponible"""
        self.ensure_one()
        if self.marble_status == 'draft':
            self.marble_status = 'available'
            _logger.info(f"Producto de mármol marcado como disponible: {self.name}")
    
    def action_set_sold(self):
        """Marcar la placa como vendida"""
        self.ensure_one()
        if self.marble_status in ['available', 'reserved']:
            self.marble_status = 'sold'
            _logger.info(f"Producto de mármol marcado como vendido: {self.name}")
    
    def action_set_damaged(self):
        """Marcar la placa como dañada"""
        self.ensure_one()
        self.marble_status = 'damaged'
        _logger.info(f"Producto de mármol marcado como dañado: {self.name}")
    
    def action_archive_marble_product(self):
        """Archivar el producto de mármol"""
        self.ensure_one()
        self.marble_status = 'archived'
        self.active = False
        _logger.info(f"Producto de mármol archivado: {self.name}")
    
    def action_view_stock_moves(self):
        """Ver movimientos de stock de este producto"""
        self.ensure_one()
        moves = self.env['stock.move'].search([
            ('product_id', '=', self.id)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Movimientos - %s') % self.name,
            'res_model': 'stock.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', moves.ids)],
            'context': {'create': False}
        }
    
    def action_view_packing_list(self):
        """Ver el packing list origen"""
        self.ensure_one()
        if self.packing_list_import_line_id:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Packing List Origen'),
                'res_model': 'packing.list.import',
                'res_id': self.packing_list_import_line_id.packing_list_id.id,
                'view_mode': 'form',
                'target': 'current'
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _('Este producto no tiene packing list asociado'),
                    'type': 'warning',
                }
            }
    
    @api.model
    def auto_archive_zero_stock_products(self):
        """
        Método para archivar automáticamente productos con stock cero
        Se puede ejecutar como cron job
        """
        products_to_archive = self.search([
            ('is_generated_marble_product', '=', True),
            ('active', '=', True),
            ('marble_status', 'in', ['available', 'sold']),
        ])
        
        archived_count = 0
        for product in products_to_archive:
            if product.current_stock <= 0:
                product.action_archive_marble_product()
                archived_count += 1
        
        _logger.info(f"Archivados automáticamente {archived_count} productos de mármol con stock cero")
        return archived_count
    
    def write(self, vals):
        """Sobrescribir write para validaciones específicas de mármol"""
        # Validar que no se pueda cambiar el estado si está vendido
        if 'marble_status' in vals and vals['marble_status'] != 'sold':
            for product in self:
                if product.marble_status == 'sold' and product.is_generated_marble_product:
                    raise ValidationError(_("No se puede cambiar el estado de un producto vendido."))
        
        return super().write(vals)
    
    @api.constrains('marble_status', 'current_stock')
    def _check_marble_status_stock(self):
        """Validar coherencia entre estado y stock"""
        for product in self:
            if product.is_generated_marble_product:
                if product.marble_status == 'sold' and product.current_stock > 0:
                    raise ValidationError(
                        _("Un producto vendido no puede tener stock positivo: %s") % product.name
                    )
                if product.marble_status == 'available' and product.current_stock <= 0:
                    _logger.warning(
                        f"Producto disponible sin stock: {product.name} "
                        f"(Stock: {product.current_stock})"
                    )
```

-e ### ./models/product_template.py
```
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Campo identificador de plantilla de mármol
    is_marble_template = fields.Boolean(
        string='Es Plantilla de Mármol',
        default=False,
        help='Indica si este producto es una plantilla base para crear productos únicos de mármol'
    )
    
    # Campos específicos del mármol - Dimensiones
    marble_height = fields.Float(
        string='Alto (cm)',
        digits=(10, 2),
        help='Alto de la placa en centímetros'
    )
    
    marble_width = fields.Float(
        string='Ancho (cm)', 
        digits=(10, 2),
        help='Ancho de la placa en centímetros'
    )
    
    marble_thickness = fields.Float(
        string='Grosor (cm)',
        digits=(10, 2),
        help='Grosor de la placa en centímetros'
    )
    
    marble_sqm = fields.Float(
        string='Metros Cuadrados',
        compute='_compute_marble_sqm',
        store=True,
        digits=(10, 4),
        help='Metros cuadrados calculados automáticamente (Alto x Ancho / 10000)'
    )
    
    # Campos de precio
    price_per_sqm = fields.Float(
        string='Precio por M²',
        digits='Product Price',
        help='Precio por metro cuadrado para cálculos automáticos'
    )
    
    # Campos adicionales para el flujo de negocio
    marble_finish = fields.Char(
        string='Acabado',
        help='Tipo de acabado (Pulido, Leather, Antique, etc.)'
    )
    
    marble_origin = fields.Char(
        string='Origen',
        help='País o región de origen del mármol'
    )
    
    marble_category = fields.Selection([
        ('marble', 'Mármol'),
        ('granite', 'Granito'),
        ('quartzite', 'Cuarcita'),
        ('limestone', 'Piedra Caliza'),
        ('travertine', 'Travertino'),
        ('onyx', 'Ónix'),
        ('other', 'Otro')
    ], string='Categoría de Piedra', default='marble')
    
    # Campo computado para contar productos generados
    generated_products_count = fields.Integer(
        string='Productos Generados',
        compute='_compute_generated_products_count',
        help='Número de productos únicos generados desde esta plantilla'
    )
    
    @api.depends('marble_height', 'marble_width')
    def _compute_marble_sqm(self):
        """Calcular metros cuadrados basado en alto y ancho"""
        for record in self:
            if record.marble_height and record.marble_width:
                # Convertir de cm² a m² (dividir por 10000)
                record.marble_sqm = (record.marble_height * record.marble_width) / 10000
            else:
                record.marble_sqm = 0.0
    
    def _compute_generated_products_count(self):
        """Calcular número de productos generados"""
        for record in self:
            if record.is_marble_template:
                generated_products = self.env['product.product'].search_count([
                    ('marble_parent_template_id', '=', record.id)
                ])
                record.generated_products_count = generated_products
            else:
                record.generated_products_count = 0
    
    @api.onchange('is_marble_template')
    def _onchange_is_marble_template(self):
        """Configurar valores por defecto para plantillas de mármol"""
        if self.is_marble_template:
            # ✅ CORRECCIÓN: Usar 'consu' (Bienes) en lugar de 'product' según la imagen.
            # 'product' (Producto Almacenable) no está disponible en tu entorno.
            self.type = 'consu'
            self.tracking = 'none'  # Las plantillas no se trackean
            
            # Buscar UoM correcta sin crear duplicados
            try:
                # 1. Intentar usar la referencia estándar de Odoo
                sqm_uom = self.env.ref('uom.product_uom_square_meter', raise_if_not_found=False)
                
                if not sqm_uom:
                    # 2. Buscar por nombre en la categoría Surface
                    surface_category = self.env.ref('uom.uom_categ_surface', raise_if_not_found=False)
                    if surface_category:
                        sqm_uom = self.env['uom.uom'].search([
                            ('category_id', '=', surface_category.id),
                            ('uom_type', '=', 'reference')
                        ], limit=1)
                
                if not sqm_uom:
                    # 3. Buscar cualquier UoM de superficie como referencia
                    sqm_uom = self.env['uom.uom'].search([
                        ('name', 'in', ['m²', 'Square Meter', 'Metro Cuadrado', 'Square Metres'])
                    ], limit=1)
                
                if sqm_uom:
                    self.uom_id = sqm_uom.id
                    self.uom_po_id = sqm_uom.id
                else:
                    # 4. Fallback: usar metros lineales
                    meter_uom = self.env.ref('uom.product_uom_meter', raise_if_not_found=False)
                    if meter_uom:
                        self.uom_id = meter_uom.id
                        self.uom_po_id = meter_uom.id
                    
            except Exception as e:
                # Si hay cualquier error, usar metros lineales como fallback seguro
                meter_uom = self.env.ref('uom.product_uom_meter', raise_if_not_found=False)
                if meter_uom:
                    self.uom_id = meter_uom.id
                    self.uom_po_id = meter_uom.id
    
    @api.constrains('marble_height', 'marble_width', 'marble_thickness')
    def _check_marble_dimensions(self):
        """Validar que las dimensiones sean positivas"""
        for record in self:
            if record.is_marble_template:
                if record.marble_height and record.marble_height <= 0:
                    raise ValidationError(_("El alto debe ser mayor a cero."))
                if record.marble_width and record.marble_width <= 0:
                    raise ValidationError(_("El ancho debe ser mayor a cero."))
                if record.marble_thickness and record.marble_thickness <= 0:
                    raise ValidationError(_("El grosor debe ser mayor a cero."))
    
    @api.constrains('is_marble_template', 'marble_sqm')
    def _check_marble_template_sqm(self):
        """Validar que las plantillas de mármol tengan metros cuadrados"""
        for record in self:
            if record.is_marble_template and not record.marble_sqm:
                raise ValidationError(_(
                    "Las plantillas de mármol deben tener dimensiones válidas para calcular los metros cuadrados."
                ))
    
    def name_get(self):
        """Personalizar el nombre mostrado para plantillas de mármol"""
        result = []
        for record in self:
            name = record.name
            if record.is_marble_template:
                name_parts = [name]
                
                if record.marble_thickness:
                    name_parts.append(f"{record.marble_thickness}cm")
                    
                if record.marble_finish:
                    name_parts.append(record.marble_finish)
                
                if record.marble_origin:
                    name_parts.append(f"({record.marble_origin})")
                
                name = " - ".join(name_parts)
            
            result.append((record.id, name))
        return result
    
    def action_view_generated_products(self):
        """Ver productos generados desde esta plantilla"""
        self.ensure_one()
        generated_products = self.env['product.product'].search([
            ('marble_parent_template_id', '=', self.id)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Productos Generados - %s') % self.name,
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', generated_products.ids)],
            'context': {
                'create': False,
                'default_marble_parent_template_id': self.id,
                'search_default_marble_products': 1,
            }
        }
    
    def action_create_marble_variant(self):
        """Crear variante manual de mármol para casos especiales"""
        self.ensure_one()
        
        if not self.is_marble_template:
            raise ValidationError(_("Solo se pueden crear variantes desde plantillas de mármol."))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Crear Variante de Mármol'),
            'res_model': 'product.product',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_tmpl_id': self.id,
                'default_is_generated_marble_product': True,
                'default_marble_parent_template_id': self.id,
                'default_marble_status': 'draft',
                'form_view_initial_mode': 'edit',
            }
        }
    
    def action_duplicate_as_template(self):
        """Duplicar como nueva plantilla de mármol"""
        self.ensure_one()
        
        copy_vals = {
            'name': _('%s (Copia)') % self.name,
            'is_marble_template': True,
        }
        
        new_template = self.copy(copy_vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Nueva Plantilla de Mármol'),
            'res_model': 'product.template',
            'res_id': new_template.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def write(self, vals):
        """Sobrescribir write para validaciones y actualizaciones automáticas"""
        # Si se cambian las dimensiones, recalcular m²
        if any(field in vals for field in ['marble_height', 'marble_width']):
            for record in self:
                if record.is_marble_template:
                    # Forzar recálculo después del write
                    result = super(ProductTemplate, record).write(vals)
                    record._compute_marble_sqm()
                    return result
        
        return super().write(vals)
    
    @api.model
    def create(self, vals):
        """Sobrescribir create para configuraciones automáticas"""
        # Si es plantilla de mármol, asegurar configuraciones
        if vals.get('is_marble_template'):
            # ✅ CORRECCIÓN: Usar 'consu' (Bienes) en lugar de 'product' según la imagen.
            vals.setdefault('type', 'consu')
            vals.setdefault('tracking', 'none')
            
            # Configurar UoM de manera segura
            if 'uom_id' not in vals or 'uom_po_id' not in vals:
                # Buscar UoM de superficie existente
                sqm_uom = self.env.ref('uom.product_uom_square_meter', raise_if_not_found=False)
                if not sqm_uom:
                    # Buscar en categoría Surface
                    surface_category = self.env.ref('uom.uom_categ_surface', raise_if_not_found=False)
                    if surface_category:
                        sqm_uom = self.env['uom.uom'].search([
                            ('category_id', '=', surface_category.id),
                            ('uom_type', '=', 'reference')
                        ], limit=1)
                
                if sqm_uom:
                    vals.setdefault('uom_id', sqm_uom.id)
                    vals.setdefault('uom_po_id', sqm_uom.id)
                else:
                    # Fallback seguro: metros lineales
                    meter_uom = self.env.ref('uom.product_uom_meter', raise_if_not_found=False)
                    if meter_uom:
                        vals.setdefault('uom_id', meter_uom.id)
                        vals.setdefault('uom_po_id', meter_uom.id)
        
        return super().create(vals)
    
    @api.model
    def search_marble_templates_by_name(self, name_pattern):
        """Búsqueda especializada para plantillas de mármol por nombre"""
        domain = [
            ('is_marble_template', '=', True),
            '|', '|', '|',
            ('name', 'ilike', name_pattern),
            ('marble_finish', 'ilike', name_pattern),
            ('marble_origin', 'ilike', name_pattern),
            ('marble_category', 'ilike', name_pattern),
        ]
        
        return self.search(domain)
    
    def get_marble_info_summary(self):
        """Obtener resumen de información de mármol para reportes"""
        self.ensure_one()
        
        if not self.is_marble_template:
            return {}
        
        return {
            'name': self.name,
            'dimensions': f"{self.marble_height} x {self.marble_width} x {self.marble_thickness} cm",
            'sqm': self.marble_sqm,
            'category': dict(self._fields['marble_category'].selection).get(self.marble_category),
            'origin': self.marble_origin or _('No especificado'),
            'finish': self.marble_finish or _('No especificado'),
            'price_per_sqm': self.price_per_sqm,
            'generated_products': self.generated_products_count,
        }
```

-e ### ./models/purchase_order_line.py
```
from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_marble_template = fields.Boolean(
        string='¿Es Mármol?',
        related='product_id.is_marble_template',
        store=True,
        readonly=True
    )
```

-e ### ./models/purchase_order.py
```
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
```

-e ### ./models/stock_picking.py
```
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
```
```

-e ### ./security/ir.model.access.csv
```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_packing_list_import_user,packing.list.import.user,model_packing_list_import,base.group_user,1,1,1,1
access_packing_list_import_line_user,packing.list.import.line.user,model_packing_list_import_line,base.group_user,1,1,1,1
access_packing_list_import_wizard_user,packing.list.import.wizard.user,model_packing_list_import_wizard,base.group_user,1,1,1,1
access_packing_list_import_manager,packing.list.import.manager,model_packing_list_import,stock.group_stock_manager,1,1,1,1
access_packing_list_import_line_manager,packing.list.import.line.manager,model_packing_list_import_line,stock.group_stock_manager,1,1,1,1
access_packing_list_import_wizard_manager,packing.list.import.wizard.manager,model_packing_list_import_wizard,stock.group_stock_manager,1,1,1,1
```

-e ### ./static/src/css/marble_styles.css
```
/* Estilos CSS para el módulo de gestión de mármol */

/* Estilos para plantillas de mármol */
.o_form_view .o_marble_template_highlight {
    background-color: #f8f9fa;
    border-left: 4px solid #28a745;
    padding: 10px;
    margin: 10px 0;
}

/* Estilos para productos únicos de mármol */
.o_marble_product_card {
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.o_marble_product_card .o_marble_serial {
    font-family: 'Courier New', monospace;
    font-weight: bold;
    color: #495057;
    background-color: #e9ecef;
    padding: 2px 6px;
    border-radius: 4px;
}

/* Estados de productos de mármol */
.o_marble_status_draft {
    color: #6c757d;
}

.o_marble_status_available {
    color: #28a745;
    font-weight: bold;
}

.o_marble_status_reserved {
    color: #ffc107;
    font-weight: bold;
}

.o_marble_status_sold {
    color: #dc3545;
    font-weight: bold;
}

.o_marble_status_damaged {
    color: #fd7e14;
    font-weight: bold;
}

.o_marble_status_archived {
    color: #6c757d;
    text-decoration: line-through;
}

/* Estilos para dimensiones */
.o_marble_dimensions {
    font-family: 'Roboto', sans-serif;
    background-color: #e3f2fd;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
    margin: 2px;
}

/* Estilos para el wizard de importación */
.o_packing_list_wizard {
    max-width: 800px;
}

.o_packing_list_preview {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 15px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    max-height: 300px;
    overflow-y: auto;
}

/* Estilos para estadísticas */
.o_marble_stats {
    display: flex;
    justify-content: space-around;
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin: 15px 0;
}

.o_marble_stat_item {
    text-align: center;
    flex: 1;
}

.o_marble_stat_number {
    font-size: 2em;
    font-weight: bold;
    color: #495057;
    display: block;
}

.o_marble_stat_label {
    font-size: 0.9em;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Estilos para la vista de lista de packing lists */
.o_list_view .o_packing_list_row {
    border-left: 3px solid transparent;
}

.o_list_view .o_packing_list_row[data-state="draft"] {
    border-left-color: #6c757d;
}

.o_list_view .o_packing_list_row[data-state="imported"] {
    border-left-color: #17a2b8;
}

.o_list_view .o_packing_list_row[data-state="processed"] {
    border-left-color: #28a745;
}

.o_list_view .o_packing_list_row[data-state="cancelled"] {
    border-left-color: #dc3545;
}

/* Estilos para botones de acción */
.o_marble_action_button {
    margin: 5px;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.o_marble_action_button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Estilos para alertas */
.o_marble_alert {
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid;
}

.o_marble_alert_success {
    background-color: #d4edda;
    color: #155724;
    border-left-color: #28a745;
}

.o_marble_alert_warning {
    background-color: #fff3cd;
    color: #856404;
    border-left-color: #ffc107;
}

.o_marble_alert_danger {
    background-color: #f8d7da;
    color: #721c24;
    border-left-color: #dc3545;
}

.o_marble_alert_info {
    background-color: #d1ecf1;
    color: #0c5460;
    border-left-color: #17a2b8;
}

/* Responsive design para móviles */
@media (max-width: 768px) {
    .o_marble_stats {
        flex-direction: column;
    }
    
    .o_marble_stat_item {
        margin: 10px 0;
    }
    
    .o_marble_product_card {
        margin: 5px 0;
        padding: 10px;
    }
}

/* Animaciones */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.o_marble_fade_in {
    animation: fadeIn 0.5s ease-out;
}

/* Estilos para formularios */
.o_marble_form_section {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.o_marble_form_section h3 {
    color: #495057;
    margin-bottom: 15px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e9ecef;
}
```

-e ### ./views/menu_views.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Menú principal de Gestión de Mármol -->
    <menuitem id="menu_marble_management" 
              name="Gestión de Mármol" 
              sequence="50"/>
    
    <!-- Submenú de Productos -->
    <menuitem id="menu_marble_products" 
              name="Productos" 
              parent="menu_marble_management" 
              sequence="10"/>
    
    <menuitem id="menu_marble_templates" 
              name="Plantillas de Mármol" 
              parent="menu_marble_products" 
              action="action_marble_templates" 
              sequence="10"/>
    
    <menuitem id="menu_marble_products_unique" 
              name="Productos Únicos" 
              parent="menu_marble_products" 
              action="action_marble_products" 
              sequence="20"/>
    
    <menuitem id="menu_marble_products_available" 
              name="Mármol Disponible" 
              parent="menu_marble_products" 
              action="action_marble_products_available" 
              sequence="30"/>
    
    <!-- Submenú de Compras -->
    <menuitem id="menu_marble_purchases" 
              name="Compras" 
              parent="menu_marble_management" 
              sequence="20"/>
    
    <menuitem id="menu_marble_purchase_orders" 
              name="Órdenes de Compra" 
              parent="menu_marble_purchases" 
              action="action_purchase_order_marble" 
              sequence="10"/>
    
    <menuitem id="menu_marble_packing_lists" 
              name="Packing Lists" 
              parent="menu_marble_purchases" 
              action="action_packing_list_import" 
              sequence="20"/>
    
    <menuitem id="menu_marble_packing_lines" 
              name="Líneas de Packing List" 
              parent="menu_marble_purchases" 
              action="action_packing_list_import_lines" 
              sequence="30"/>
    
    <!-- Añadir elementos al menú de Inventario existente -->
    <menuitem id="menu_marble_inventory_products" 
              name="Productos de Mármol" 
              parent="stock.menu_stock_inventory_control" 
              action="action_marble_products_available" 
              sequence="15"/>
    
    <!-- Añadir elementos al menú de Compras existente -->
    <menuitem id="menu_marble_purchase_orders_std" 
              name="Órdenes de Mármol" 
              parent="purchase.menu_purchase_root" 
              action="action_purchase_order_marble" 
              sequence="15"/>

</odoo>
```

-e ### ./views/packing_list_import_views.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Vista de formulario para packing list import -->
    <record id="packing_list_import_form_view" model="ir.ui.view">
        <field name="name">packing.list.import.form</field>
        <field name="model">packing.list.import</field>
        <field name="arch" type="xml">
            <form string="Packing List">
                <header>
                    <button name="action_process_packing_list" string="Procesar Packing List" 
                            type="object" class="btn-primary"
                            invisible="state != 'imported'"/>
                    <button name="action_cancel" string="Cancelar" 
                            type="object" class="btn-secondary"
                            invisible="state in ['processed', 'cancelled']"/>
                    <button name="action_set_to_draft" string="Volver a Borrador" 
                            type="object" class="btn-secondary"
                            invisible="state not in ['imported', 'cancelled']"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,imported,processed"/>
                </header>
                
                <sheet>
                    <div class="oe_button_box" name="button_box">
                        <button name="action_view_created_products" type="object" 
                                class="oe_stat_button" icon="fa-cubes"
                                invisible="created_products_count == 0">
                            <field name="created_products_count" widget="statinfo" string="Productos Creados"/>
                        </button>
                    </div>
                    
                    <div class="oe_title">
                        <h1>
                            <field name="display_name" readonly="1"/>
                        </h1>
                    </div>
                    
                    <group>
                        <group string="Información General">
                            <field name="name"/>
                            <field name="purchase_order_id" readonly="1"/>
                            <field name="supplier_id" readonly="1"/>
                        </group>
                        <group string="Información del Envío">
                            <field name="container_number"/>
                            <field name="commercial_invoice"/>
                            <field name="import_date" readonly="1"/>
                            <field name="process_date" readonly="1"/>
                        </group>
                    </group>
                    
                    <group string="Resumen Estadístico">
                        <group>
                            <field name="total_pieces" readonly="1"/>
                            <field name="total_sqm" readonly="1"/>
                        </group>
                        <group>
                            <field name="total_lots" readonly="1"/>
                            <field name="total_crates" readonly="1"/>
                        </group>
                    </group>
                    
                    <notebook>
                        <page string="Líneas del Packing List" name="lines">
                            <field name="line_ids">
                                <list string="Líneas" editable="bottom" create="true" delete="true">
                                    <field name="product_name"/>
                                    <field name="marble_height"/>
                                    <field name="marble_width"/>
                                    <field name="marble_thickness"/>
                                    <field name="marble_sqm" readonly="1"/>
                                    <field name="marble_custom_lot"/>
                                    <field name="wooden_crate_code"/>
                                    <field name="supplier_lot_number"/>
                                    <field name="marble_finish"/>
                                    <field name="cost_price"/>
                                    <field name="price_per_sqm"/>
                                    <field name="created_product_id" readonly="1"/>
                                    <field name="is_processed" readonly="1"/>
                                </list>
                                <form string="Línea de Packing List">
                                    <sheet>
                                        <group>
                                            <group string="Producto">
                                                <field name="product_name"/>
                                                <field name="marble_finish"/>
                                            </group>
                                            <group string="Estado">
                                                <field name="is_processed" readonly="1"/>
                                                <field name="created_product_id" readonly="1"/>
                                            </group>
                                        </group>
                                        
                                        <group string="Dimensiones">
                                            <group>
                                                <field name="marble_height"/>
                                                <field name="marble_width"/>
                                                <field name="marble_thickness"/>
                                            </group>
                                            <group>
                                                <field name="marble_sqm" readonly="1"/>
                                            </group>
                                        </group>
                                        
                                        <group string="Trazabilidad">
                                            <group>
                                                <field name="marble_custom_lot"/>
                                                <field name="wooden_crate_code"/>
                                            </group>
                                            <group>
                                                <field name="supplier_lot_number"/>
                                            </group>
                                        </group>
                                        
                                        <group string="Precio">
                                            <group>
                                                <field name="cost_price"/>
                                                <field name="price_per_sqm"/>
                                            </group>
                                        </group>
                                        
                                        <group string="Errores" invisible="not has_errors">
                                            <field name="has_errors" readonly="1"/>
                                            <field name="error_message" readonly="1"/>
                                        </group>
                                    </sheet>
                                </form>
                            </field>
                        </page>
                        
                        <page string="Notas" name="notes">
                            <field name="notes" placeholder="Notas adicionales sobre este packing list..."/>
                        </page>
                    </notebook>
                </sheet>
                
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>
    
    <!-- Vista de lista para packing list import -->
    <record id="packing_list_import_list_view" model="ir.ui.view">
        <field name="name">packing.list.import.list</field>
        <field name="model">packing.list.import</field>
        <field name="arch" type="xml">
            <list string="Packing Lists">
                <field name="name"/>
                <field name="purchase_order_id"/>
                <field name="supplier_id"/>
                <field name="container_number"/>
                <field name="commercial_invoice"/>
                <field name="state" decoration-success="state == 'processed'" 
                       decoration-info="state == 'imported'" decoration-muted="state == 'cancelled'"/>
                <field name="total_pieces"/>
                <field name="total_sqm"/>
                <field name="total_lots"/>
                <field name="import_date"/>
                <field name="created_products_count"/>
            </list>
        </field>
    </record>
    
    <!-- Vista de búsqueda para packing list import -->
    <record id="packing_list_import_search_view" model="ir.ui.view">
        <field name="name">packing.list.import.search</field>
        <field name="model">packing.list.import</field>
        <field name="arch" type="xml">
            <search string="Buscar Packing Lists">
                <field name="name"/>
                <field name="purchase_order_id"/>
                <field name="supplier_id"/>
                <field name="container_number"/>
                <field name="commercial_invoice"/>
                
                <filter string="Borradores" name="draft" domain="[('state', '=', 'draft')]"/>
                <filter string="Importados" name="imported" domain="[('state', '=', 'imported')]"/>
                <filter string="Procesados" name="processed" domain="[('state', '=', 'processed')]"/>
                <filter string="Cancelados" name="cancelled" domain="[('state', '=', 'cancelled')]"/>
                
                <separator/>
                <filter string="Últimos 30 días" name="last_month" 
                        domain="[('import_date', '&gt;=', (context_today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d'))]"/>
                
                <group expand="0" string="Agrupar por">
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                    <filter string="Proveedor" name="group_supplier" context="{'group_by': 'supplier_id'}"/>
                    <filter string="Orden de Compra" name="group_purchase_order" context="{'group_by': 'purchase_order_id'}"/>
                    <filter string="Fecha de Importación" name="group_import_date" context="{'group_by': 'import_date:month'}"/>
                </group>
            </search>
        </field>
    </record>
    
    <!-- Acción principal para packing lists -->
    <record id="action_packing_list_import" model="ir.actions.act_window">
        <field name="name">Packing Lists</field>
        <field name="res_model">packing.list.import</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No hay packing lists importados
            </p>
            <p>
                Los packing lists se crean desde las órdenes de compra de mármol
                utilizando el botón "Importar Packing List".
            </p>
        </field>
    </record>
    
    <!-- Vista de líneas de packing list (independiente) -->
    <record id="packing_list_import_line_list_view" model="ir.ui.view">
        <field name="name">packing.list.import.line.list</field>
        <field name="model">packing.list.import.line</field>
        <field name="arch" type="xml">
            <list string="Líneas de Packing List">
                <field name="packing_list_id"/>
                <field name="product_name"/>
                <field name="marble_height"/>
                <field name="marble_width"/>
                <field name="marble_thickness"/>
                <field name="marble_sqm"/>
                <field name="marble_custom_lot"/>
                <field name="wooden_crate_code"/>
                <field name="supplier_lot_number"/>
                <field name="created_product_id"/>
                <field name="is_processed" decoration-success="is_processed == True"/>
            </list>
        </field>
    </record>
    
    <!-- Vista de formulario para líneas de packing list -->
    <record id="packing_list_import_line_form_view" model="ir.ui.view">
        <field name="name">packing.list.import.line.form</field>
        <field name="model">packing.list.import.line</field>
        <field name="arch" type="xml">
            <form string="Línea de Packing List">
                <header>
                    <button name="action_view_created_product" string="Ver Producto Creado" 
                            type="object" class="btn-primary"
                            invisible="not created_product_id"/>
                    <field name="is_processed" widget="statusbar" statusbar_visible="False,True"/>
                </header>
                
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="product_name"/>
                        </h1>
                    </div>
                    
                    <group>
                        <group string="Packing List">
                            <field name="packing_list_id"/>
                        </group>
                        <group string="Producto Creado">
                            <field name="created_product_id" readonly="1"/>
                        </group>
                    </group>
                    
                    <group string="Dimensiones">
                        <group>
                            <field name="marble_height"/>
                            <field name="marble_width"/>
                            <field name="marble_thickness"/>
                        </group>
                        <group>
                            <field name="marble_sqm" readonly="1"/>
                            <field name="marble_finish"/>
                        </group>
                    </group>
                    
                    <group string="Trazabilidad">
                        <group>
                            <field name="marble_custom_lot"/>
                            <field name="wooden_crate_code"/>
                        </group>
                        <group>
                            <field name="supplier_lot_number"/>
                        </group>
                    </group>
                    
                    <group string="Precio">
                        <group>
                            <field name="cost_price"/>
                            <field name="price_per_sqm"/>
                        </group>
                    </group>
                    
                    <group string="Control de Errores" invisible="not has_errors">
                        <field name="has_errors" readonly="1"/>
                        <field name="error_message" readonly="1"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
    
    <!-- Acción para líneas de packing list -->
    <record id="action_packing_list_import_lines" model="ir.actions.act_window">
        <field name="name">Líneas de Packing List</field>
        <field name="res_model">packing.list.import.line</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No hay líneas de packing list
            </p>
        </field>
    </record>

</odoo>
```

-e ### ./views/packing_list_import_wizard_views.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Vista del wizard para importar packing list -->
    <record id="packing_list_import_wizard_form" model="ir.ui.view">
        <field name="name">packing.list.import.wizard.form</field>
        <field name="model">packing.list.import.wizard</field>
        <field name="arch" type="xml">
            <form string="Importar Packing List">
                <header>
                    <button name="action_import_packing_list" string="Importar" 
                            type="object" class="btn-primary"
                            invisible="step == 'upload'"/>
                    <button name="action_generate_template" string="Descargar Plantilla CSV" 
                            type="object" class="btn-secondary"/>
                    <button name="action_show_json_example" string="Ejemplo JSON" 
                            type="object" class="btn-secondary"
                            invisible="import_method != 'manual'"/>
                    <field name="step" widget="statusbar" statusbar_visible="upload,preview,import"/>
                </header>
                
                <sheet>
                    <div class="oe_title">
                        <h1>Importar Packing List</h1>
                        <h2>
                            <field name="purchase_order_id" readonly="1"/>
                        </h2>
                    </div>
                    
                    <group>
                        <group string="Información del Envío">
                            <field name="container_number" required="1"/>
                            <field name="commercial_invoice" required="1"/>
                            <field name="packing_list_name"/>
                        </group>
                        <group string="Método de Importación">
                            <field name="import_method" widget="radio"/>
                        </group>
                    </group>
                    
                    <!-- Sección para carga de archivo -->
                    <div invisible="import_method not in ['csv', 'excel']">
                        <separator string="Cargar Archivo"/>
                        <group>
                            <group>
                                <field name="import_file" filename="filename" 
                                       required="import_method in ['csv', 'excel']"/>
                                <field name="filename" invisible="1"/>
                            </group>
                            <group invisible="import_method != 'csv'">
                                <field name="has_header"/>
                                <field name="delimiter"/>
                            </group>
                        </group>
                        
                        <!-- Vista previa del archivo -->
                        <div invisible="not preview_data">
                            <separator string="Vista Previa del Archivo"/>
                            <field name="preview_data" widget="text" readonly="1" 
                                   style="font-family: monospace; white-space: pre;"/>
                        </div>
                    </div>
                    
                    <!-- Sección para entrada manual -->
                    <div invisible="import_method != 'manual'">
                        <separator string="Datos Manuales (JSON)"/>
                        <div class="alert alert-info" role="alert">
                            <strong>Formato esperado:</strong> Lista de objetos JSON con los campos requeridos.
                            Use el botón "Ejemplo JSON" para ver el formato correcto.
                        </div>
                        <field name="manual_data" widget="ace" options="{'mode': 'json'}" 
                               required="import_method == 'manual'"/>
                    </div>
                    
                    <!-- Información de ayuda -->
                    <div class="alert alert-warning" role="alert">
                        <h4>Campos Requeridos para Importación:</h4>
                        <ul>
                            <li><strong>product_name:</strong> Nombre del material (ej: Amazon-2cm-Leather)</li>
                            <li><strong>height:</strong> Alto en centímetros</li>
                            <li><strong>width:</strong> Ancho en centímetros</li>
                            <li><strong>thickness:</strong> Grosor en centímetros</li>
                            <li><strong>lot:</strong> Lote personalizado/Wooden Crate</li>
                            <li><strong>wooden_crate:</strong> Código de atado</li>
                            <li><strong>supplier_lot:</strong> Número de lote del proveedor</li>
                        </ul>
                        <h4>Campos Opcionales:</h4>
                        <ul>
                            <li><strong>cost:</strong> Costo unitario</li>
                            <li><strong>price_per_sqm:</strong> Precio por metro cuadrado</li>
                            <li><strong>finish:</strong> Acabado (Leather, Polished, etc.)</li>
                        </ul>
                    </div>
                </sheet>
            </form>
        </field>
    </record>
    
    <!-- Vista de lista para wizard (para debugging/admin) -->
    <record id="packing_list_import_wizard_list" model="ir.ui.view">
        <field name="name">packing.list.import.wizard.list</field>
        <field name="model">packing.list.import.wizard</field>
        <field name="arch" type="xml">
            <list string="Wizards de Importación">
                <field name="purchase_order_id"/>
                <field name="container_number"/>
                <field name="commercial_invoice"/>
                <field name="import_method"/>
                <field name="step"/>
                <field name="create_date"/>
            </list>
        </field>
    </record>
    
    <!-- Acción del wizard -->
    <record id="action_packing_list_import_wizard" model="ir.actions.act_window">
        <field name="name">Importar Packing List</field>
        <field name="res_model">packing.list.import.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>

    <!-- Acción adicional para vista de administración -->
    <record id="action_packing_list_import_wizard_admin" model="ir.actions.act_window">
        <field name="name">Wizards de Importación (Admin)</field>
        <field name="res_model">packing.list.import.wizard</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'create': False}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No hay wizards de importación registrados
            </p>
            <p>
                Esta vista es solo para administradores para revisar
                el historial de importaciones de packing lists.
            </p>
        </field>
    </record>

</odoo>
```

-e ### ./views/product_product_views.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Vista de formulario para productos únicos de mármol -->
    <record id="product_product_form_view_marble" model="ir.ui.view">
        <field name="name">product.product.form.marble</field>
        <field name="model">product.product</field>
        <field name="inherit_id" ref="product.product_normal_form_view"/>
        <field name="priority">99</field>
        <field name="arch" type="xml">
            
            <!-- Ocultar botón problemático heredado de product.template -->
            <xpath expr="//button[@name='action_view_generated_products']" position="replace"/>
            
            <!-- Campos específicos de mármol después del código de barras -->
            <xpath expr="//field[@name='barcode']" position="after">
                <field name="is_generated_marble_product" invisible="1"/>
                <field name="marble_serial_number" readonly="1"
                       invisible="not is_generated_marble_product"/>
                <field name="marble_status" 
                       invisible="not is_generated_marble_product"/>
            </xpath>

            <!-- Botones estadísticos específicos para mármol -->
            <xpath expr="//div[@name='button_box']" position="inside">
                <button name="action_view_stock_moves" type="object" 
                        class="oe_stat_button" icon="fa-exchange"
                        invisible="not is_generated_marble_product">
                    <div class="o_field_widget o_stat_info">
                        <span class="o_stat_text">Movimientos</span>
                    </div>
                </button>
                <button name="action_view_packing_list" type="object" 
                        class="oe_stat_button" icon="fa-list-alt"
                        invisible="not is_generated_marble_product or not packing_list_import_line_id">
                    <div class="o_field_widget o_stat_info">
                        <span class="o_stat_text">Packing List</span>
                    </div>
                </button>
            </xpath>

            <!-- Pestaña de información de mármol -->
            <xpath expr="//page[@name='general_information']" position="after">
                <page string="Información de Mármol" name="marble_info" 
                      invisible="not is_generated_marble_product">
                    <group>
                        <group string="Dimensiones Específicas">
                            <field name="marble_height" readonly="1"/>
                            <field name="marble_width" readonly="1"/>
                            <field name="marble_thickness" readonly="1"/>
                            <field name="marble_sqm" readonly="1"/>
                        </group>
                        <group string="Características">
                            <field name="marble_category" readonly="1"/>
                            <field name="marble_finish" readonly="1"/>
                            <field name="marble_origin" readonly="1"/>
                            <field name="price_per_sqm" readonly="1"/>
                        </group>
                    </group>
                    <group string="Trazabilidad Completa">
                        <group>
                            <field name="marble_custom_lot" readonly="1"/>
                            <field name="wooden_crate_code" readonly="1"/>
                            <field name="supplier_lot_number" readonly="1"/>
                        </group>
                        <group>
                            <field name="container_number" readonly="1"/>
                            <field name="commercial_invoice" readonly="1"/>
                            <field name="marble_creation_date" readonly="1"/>
                        </group>
                    </group>
                    <group string="Referencias">
                        <field name="marble_parent_template_id" readonly="1"/>
                        <field name="packing_list_import_line_id" readonly="1"/>
                    </group>
                    <group string="Stock Actual">
                        <field name="current_stock" readonly="1"/>
                    </group>
                </page>
            </xpath>

            <!-- Botones de acción en el header -->
            <xpath expr="//header" position="inside">
                <button name="action_set_available" string="Marcar Disponible" 
                        type="object" class="btn-primary"
                        invisible="not is_generated_marble_product or marble_status != 'draft'"/>
                <button name="action_set_sold" string="Marcar Vendido" 
                        type="object" class="btn-secondary"
                        invisible="not is_generated_marble_product or marble_status not in ['available', 'reserved']"/>
                <button name="action_set_damaged" string="Marcar Dañado" 
                        type="object" class="btn-warning"
                        invisible="not is_generated_marble_product"/>
                <button name="action_archive_marble_product" string="Archivar" 
                        type="object" class="btn-danger"
                        invisible="not is_generated_marble_product"/>
            </xpath>
        </field>
    </record>

    <!-- Vista de lista para productos únicos de mármol -->
    <record id="product_product_list_view_marble" model="ir.ui.view">
        <field name="name">product.product.list.marble</field>
        <field name="model">product.product</field>
        <field name="inherit_id" ref="product.product_product_tree_view"/>
        <field name="arch" type="xml">
            <!-- Campo invisible para condiciones -->
            <xpath expr="//field[@name='name']" position="before">
                <field name="is_generated_marble_product" column_invisible="1"/>
            </xpath>
            
            <!-- Campos específicos de mármol -->
            <xpath expr="//field[@name='name']" position="after">
                <field name="marble_serial_number" optional="hide"
                       column_invisible="not parent.is_generated_marble_product"/>
                <field name="marble_status" optional="hide"
                       column_invisible="not parent.is_generated_marble_product"/>
                <field name="marble_sqm" optional="hide"
                       column_invisible="not parent.is_generated_marble_product"/>
                <field name="marble_custom_lot" optional="hide"
                       column_invisible="not parent.is_generated_marble_product"/>
                <field name="current_stock" optional="hide"
                       column_invisible="not parent.is_generated_marble_product"/>
            </xpath>
        </field>
    </record>

    <!-- Vista kanban para productos de mármol -->
    <record id="product_product_kanban_view_marble" model="ir.ui.view">
        <field name="name">product.product.kanban.marble</field>
        <field name="model">product.product</field>
        <field name="arch" type="xml">
            <kanban>
                <field name="id"/>
                <field name="name"/>
                <field name="image_128"/>
                <field name="is_generated_marble_product"/>
                <field name="marble_serial_number"/>
                <field name="marble_status"/>
                <field name="marble_sqm"/>
                <field name="marble_custom_lot"/>
                <field name="current_stock"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_global_click">
                            <div class="o_kanban_image">
                                <img t-att-src="kanban_image('product.product', 'image_128', record.id.raw_value)" alt="Product"/>
                            </div>
                            <div class="oe_kanban_details">
                                <strong class="o_kanban_record_title">
                                    <field name="name"/>
                                </strong>
                                <div t-if="record.is_generated_marble_product.raw_value" class="o_marble_product_badge">
                                    <span class="badge badge-info">Producto Mármol</span>
                                </div>
                                <div t-if="record.is_generated_marble_product.raw_value and record.marble_serial_number.value" class="text-muted">
                                    Serie: <t t-esc="record.marble_serial_number.value"/>
                                </div>
                                <div t-if="record.is_generated_marble_product.raw_value and record.marble_status.value" class="text-muted">
                                    Estado: <t t-esc="record.marble_status.value"/>
                                </div>
                                <div t-if="record.is_generated_marble_product.raw_value and record.marble_sqm.value" class="text-muted">
                                    <t t-esc="record.marble_sqm.value"/> m²
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Filtros de búsqueda para productos de mármol -->
    <record id="product_product_search_view_marble" model="ir.ui.view">
        <field name="name">product.product.search.marble</field>
        <field name="model">product.product</field>
        <field name="inherit_id" ref="product.product_search_form_view"/>
        <field name="arch" type="xml">
            <!-- Filtros específicos para mármol -->
            <xpath expr="//filter[@name='inactive']" position="after">
                <separator/>
                <filter string="Productos de Mármol" name="marble_products" 
                        domain="[('is_generated_marble_product', '=', True)]"/>
                <filter string="Disponibles" name="marble_available" 
                        domain="[('is_generated_marble_product', '=', True), ('marble_status', '=', 'available')]"/>
                <filter string="Vendidos" name="marble_sold" 
                        domain="[('is_generated_marble_product', '=', True), ('marble_status', '=', 'sold')]"/>
                <filter string="Con Stock" name="marble_in_stock" 
                        domain="[('is_generated_marble_product', '=', True), ('current_stock', '>', 0)]"/>
                <filter string="Reservados" name="marble_reserved" 
                        domain="[('is_generated_marble_product', '=', True), ('marble_status', '=', 'reserved')]"/>
                <filter string="Dañados" name="marble_damaged" 
                        domain="[('is_generated_marble_product', '=', True), ('marble_status', '=', 'damaged')]"/>
            </xpath>
            
            <!-- Campos de búsqueda específicos -->
            <xpath expr="//field[@name='name']" position="after">
                <field name="marble_serial_number"/>
                <field name="marble_custom_lot"/>
                <field name="wooden_crate_code"/>
                <field name="supplier_lot_number"/>
                <field name="marble_status"/>
                <field name="marble_origin"/>
            </xpath>
            
            <!-- Agrupadores para mármol -->
            <xpath expr="//group/filter[@name='categ_id']" position="after">
                <filter string="Estado de Mármol" name="group_marble_status" 
                        context="{'group_by': 'marble_status'}"
                        domain="[('is_generated_marble_product', '=', True)]"/>
                <filter string="Lote Personalizado" name="group_marble_lot" 
                        context="{'group_by': 'marble_custom_lot'}"
                        domain="[('is_generated_marble_product', '=', True)]"/>
                <filter string="Plantilla Padre" name="group_parent_template" 
                        context="{'group_by': 'marble_parent_template_id'}"
                        domain="[('is_generated_marble_product', '=', True)]"/>
                <filter string="Origen" name="group_marble_origin" 
                        context="{'group_by': 'marble_origin'}"
                        domain="[('is_generated_marble_product', '=', True)]"/>
                <filter string="Categoría" name="group_marble_category" 
                        context="{'group_by': 'marble_category'}"
                        domain="[('is_generated_marble_product', '=', True)]"/>
            </xpath>
        </field>
    </record>

    <!-- Acción para productos únicos de mármol -->
    <record id="action_marble_products" model="ir.actions.act_window">
        <field name="name">Productos de Mármol</field>
        <field name="res_model">product.product</field>
        <field name="view_mode">kanban,list,form</field>
        <field name="domain">[('is_generated_marble_product', '=', True)]</field>
        <field name="view_ids" eval="[(5, 0, 0),
                                     (0, 0, {'view_mode': 'kanban', 'view_id': ref('product_product_kanban_view_marble')}),
                                     (0, 0, {'view_mode': 'list', 'view_id': ref('product_product_list_view_marble')}),
                                     (0, 0, {'view_mode': 'form', 'view_id': ref('product_product_form_view_marble')})]"/>
        <field name="context">{'search_default_marble_available': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No hay productos de mármol creados aún
            </p>
            <p>
                Los productos únicos de mármol se crean automáticamente cuando se
                procesa un packing list desde una orden de compra.
                <br/>
                Cada producto representa una placa individual con sus dimensiones,
                número de serie y trazabilidad específicos.
            </p>
        </field>
    </record>

    <!-- Acción para productos de mármol disponibles -->
    <record id="action_marble_products_available" model="ir.actions.act_window">
        <field name="name">Mármol Disponible</field>
        <field name="res_model">product.product</field>
        <field name="view_mode">kanban,list,form</field>
        <field name="domain">[('is_generated_marble_product', '=', True), ('marble_status', '=', 'available'), ('current_stock', '>', 0)]</field>
        <field name="view_ids" eval="[(5, 0, 0),
                                     (0, 0, {'view_mode': 'kanban', 'view_id': ref('product_product_kanban_view_marble')}),
                                     (0, 0, {'view_mode': 'list', 'view_id': ref('product_product_list_view_marble')}),
                                     (0, 0, {'view_mode': 'form', 'view_id': ref('product_product_form_view_marble')})]"/>
        <field name="context">{'create': False}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No hay productos de mármol disponibles
            </p>
            <p>
                Aquí se mostrarán las placas de mármol que están disponibles
                para venta y tienen stock positivo.
            </p>
        </field>
    </record>

    <!-- Acción para productos de mármol por estado -->
    <record id="action_marble_products_by_status" model="ir.actions.act_window">
        <field name="name">Mármol por Estado</field>
        <field name="res_model">product.product</field>
        <field name="view_mode">kanban,list,form</field>
        <field name="domain">[('is_generated_marble_product', '=', True)]</field>
        <field name="view_ids" eval="[(5, 0, 0),
                                     (0, 0, {'view_mode': 'kanban', 'view_id': ref('product_product_kanban_view_marble')}),
                                     (0, 0, {'view_mode': 'list', 'view_id': ref('product_product_list_view_marble')}),
                                     (0, 0, {'view_mode': 'form', 'view_id': ref('product_product_form_view_marble')})]"/>
        <field name="context">{'search_default_group_marble_status': 1, 'create': False}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No hay productos de mármol
            </p>
            <p>
                Vista agrupada por estado de las placas de mármol.
            </p>
        </field>
    </record>

</odoo>
```

-e ### ./views/product_template_views.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Vista de formulario del producto template para mármol -->
    <record id="product_template_form_view_marble" model="ir.ui.view">
        <field name="name">product.template.form.marble</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_form_view"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='categ_id']" position="after">
                <field name="is_marble_template" widget="boolean_toggle"/>
            </xpath>
            <xpath expr="//notebook" position="inside">
                <page string="Detalles de Mármol" name="marble_details" invisible="not is_marble_template">
                    <group>
                        <group string="Dimensiones Base">
                            <field name="marble_height" required="is_marble_template"/>
                            <field name="marble_width" required="is_marble_template"/>
                            <field name="marble_thickness" required="is_marble_template"/>
                            <field name="marble_sqm" readonly="1"/>
                        </group>
                        <group string="Características">
                            <field name="marble_category"/>
                            <field name="marble_finish"/>
                            <field name="marble_origin"/>
                            <field name="price_per_sqm"/>
                        </group>
                    </group>
                    <group>
                        <button name="action_view_generated_products" type="object" 
                                class="oe_stat_button" icon="fa-cubes"
                                invisible="not is_marble_template">
                            <div class="o_field_widget o_stat_info">
                                <field name="generated_products_count" widget="statinfo" string="Productos Generados"/>
                            </div>
                        </button>
                    </group>
                </page>
            </xpath>
            <xpath expr="//page[@name='inventory']" position="attributes">
                <attribute name="invisible">is_marble_template</attribute>
            </xpath>
            <xpath expr="//notebook" position="inside">
                <page string="Configuración de Inventario" name="marble_inventory" 
                      invisible="not is_marble_template">
                    <group>
                        <group string="Configuración">
                            <field name="type" readonly="1"/>
                            <field name="tracking" readonly="1"/>
                            <field name="uom_id" readonly="1"/>
                            <field name="uom_po_id" readonly="1"/>
                        </group>
                        <group string="Costos">
                            <field name="standard_price"/>
                            <field name="currency_id" invisible="1"/>
                        </group>
                    </group>
                    <div class="alert alert-info" role="alert">
                        <strong>Nota:</strong> Las plantillas de mármol se configuran automáticamente para ser productos almacenables sin seguimiento. 
                        Los productos únicos generados tendrán seguimiento por número de serie.
                    </div>
                </page>
            </xpath>
        </field>
    </record>
    
    <!-- Vista de lista para plantillas de mármol -->
    <record id="product_template_list_view_marble" model="ir.ui.view">
        <field name="name">product.template.list.marble</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_tree_view"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='name']" position="after">
                <field name="is_marble_template" optional="hide"/>
                <field name="marble_thickness" optional="hide" 
                       invisible="not is_marble_template"/>
                <field name="marble_category" optional="hide"
                       invisible="not is_marble_template"/>
                <field name="marble_origin" optional="hide"
                       invisible="not is_marble_template"/>
                <field name="marble_sqm" optional="hide"
                       invisible="not is_marble_template"/>
                <field name="price_per_sqm" optional="hide"
                       invisible="not is_marble_template"/>
            </xpath>
        </field>
    </record>
    
    <!-- Vista de búsqueda para plantillas de mármol -->
    <record id="product_template_search_view_marble" model="ir.ui.view">
        <field name="name">product.template.search.marble</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_search_view"/>
        <field name="arch" type="xml">
            <!-- Filtros tipo mármol -->
            <xpath expr="//filter[@name='filter_to_sell']" position="after">
                <separator/>
                <filter string="Plantillas de Mármol" name="marble_templates" 
                        domain="[('is_marble_template', '=', True)]"/>
                <filter string="Productos Estándar" name="standard_products" 
                        domain="[('is_marble_template', '=', False)]"/>
            </xpath>
            <!-- Campos adicionales para búsqueda -->
            <xpath expr="//field[@name='name']" position="after">
                <field name="marble_category"/>
                <field name="marble_origin"/>
                <field name="marble_finish"/>
            </xpath>
            <!-- Agrupadores existentes + mármol -->
            <xpath expr="//group/filter[@name='categ_id']" position="after">
                <filter string="Categoría de Mármol" name="group_marble_category" 
                    context="{'group_by': 'marble_category'}"
                    domain="[('is_marble_template', '=', True)]"/>
                <filter string="Origen" name="group_marble_origin" 
                    context="{'group_by': 'marble_origin'}"
                    domain="[('is_marble_template', '=', True)]"/>
                <filter string="Grosor" name="group_marble_thickness" 
                    context="{'group_by': 'marble_thickness'}"
                    domain="[('is_marble_template', '=', True)]"/>
            </xpath>
        </field>
    </record>
    
    <!-- Vista de kanban SIMPLIFICADA para plantillas de mármol -->
    <record id="product_template_kanban_view_marble" model="ir.ui.view">
        <field name="name">product.template.kanban.marble</field>
        <field name="model">product.template</field>
        <field name="arch" type="xml">
            <kanban>
                <field name="is_marble_template"/>
                <field name="marble_thickness"/>
                <field name="marble_origin"/>
                <field name="marble_category"/>
                <field name="marble_sqm"/>
                <field name="price_per_sqm"/>
                <field name="generated_products_count"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_global_click">
                            <div class="o_kanban_image">
                                <img t-att-src="kanban_image('product.template', 'image_128', record.id.raw_value)" alt="Product"/>
                            </div>
                            <div class="oe_kanban_details">
                                <strong class="o_kanban_record_title">
                                    <field name="name"/>
                                </strong>
                                <div t-if="record.is_marble_template.raw_value" class="o_marble_template_badge">
                                    <span class="badge badge-info">Plantilla Mármol</span>
                                </div>
                                <div t-if="record.is_marble_template.raw_value and record.marble_thickness.value" class="text-muted">
                                    Grosor: <t t-esc="record.marble_thickness.value"/>cm
                                </div>
                                <div t-if="record.is_marble_template.raw_value and record.marble_origin.value" class="text-muted">
                                    Origen: <t t-esc="record.marble_origin.value"/>
                                </div>
                                <div t-if="record.is_marble_template.raw_value and record.marble_sqm.value" class="text-muted">
                                    <t t-esc="record.marble_sqm.value"/> m²
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>
    
    <!-- Acción principal para plantillas de mármol -->
    <record id="action_marble_templates" model="ir.actions.act_window">
        <field name="name">Plantillas de Mármol</field>
        <field name="res_model">product.template</field>
        <field name="view_mode">kanban,list,form</field>
        <field name="domain">[('is_marble_template', '=', True)]</field>
        <field name="view_id" ref="product_template_kanban_view_marble"/>
        <field name="context">{
            'default_is_marble_template': True,
            'default_type': 'consu',
            'default_tracking': 'none',
            'search_default_marble_templates': 1,
        }</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear nueva plantilla de mármol
            </p>
            <p>
                Las plantillas de mármol son productos base que se utilizan para
                generar automáticamente productos únicos cuando se procesa un packing list.
                <br/>
                Cada plantilla define las características generales del material:
                categoría, origen, acabado típico, etc.
            </p>
        </field>
    </record>
    
    <!-- Acción para ver todas las plantillas (mármol y estándar) -->
    <record id="action_product_templates_all" model="ir.actions.act_window">
        <field name="name">Todas las Plantillas</field>
        <field name="res_model">product.template</field>
        <field name="view_mode">kanban,list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear nuevo producto
            </p>
            <p>
                Aquí puedes ver tanto plantillas de mármol como productos estándar.
                Usa los filtros para distinguir entre tipos.
            </p>
        </field>
    </record>
    
    <!-- Servidor de acciones para convertir producto a plantilla de mármol -->
    <record id="action_convert_to_marble_template" model="ir.actions.server">
        <field name="name">Convertir a Plantilla de Mármol</field>
        <field name="model_id" ref="product.model_product_template"/>
        <field name="binding_model_id" ref="product.model_product_template"/>
        <field name="state">code</field>
        <field name="code">
if records:
    for record in records:
        if not record.is_marble_template:
            record.write({
                'is_marble_template': True,
                'type': 'consu',
                'tracking': 'none',
            })
        </field>
    </record>
    
    <!-- Servidor de acciones para revertir plantilla de mármol -->
    <record id="action_revert_marble_template" model="ir.actions.server">
        <field name="name">Revertir Plantilla de Mármol</field>
        <field name="model_id" ref="product.model_product_template"/>
        <field name="binding_model_id" ref="product.model_product_template"/>
        <field name="state">code</field>
        <field name="code">
if records:
    for record in records:
        if record.is_marble_template:
            # Verificar que no tenga productos generados
            generated_products = env['product.product'].search([
                ('marble_parent_template_id', '=', record.id)
            ])
            if generated_products:
                raise UserError("No se puede revertir: tiene productos generados asociados")
            
            record.write({
                'is_marble_template': False,
                'marble_height': 0,
                'marble_width': 0,
                'marble_thickness': 0,
                'marble_custom_lot': '',
                'wooden_crate_code': '',
                'marble_finish': '',
                'marble_origin': '',
                'marble_category': 'marble',
                'price_per_sqm': 0,
            })
        </field>
    </record>
</odoo>
```

-e ### ./views/purchase_order_views.xml
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Vista de formulario de orden de compra con campos de mármol -->
    <record id="purchase_order_form_view_marble" model="ir.ui.view">
        <field name="name">purchase.order.form.marble</field>
        <field name="model">purchase.order</field>
        <field name="inherit_id" ref="purchase.purchase_order_form"/>
        <field name="arch" type="xml">
            <!-- Añadir campos de mármol en la cabecera -->
            <xpath expr="//field[@name='currency_id']" position="after">
                <field name="has_marble_products" invisible="1"/>
                <field name="container_number" invisible="not has_marble_products"/>
                <field name="commercial_invoice" invisible="not has_marble_products"/>
                <field name="packing_list_imported" readonly="1" invisible="not has_marble_products"/>
            </xpath>
            <!-- Añadir botones estadísticos -->
            <xpath expr="//div[@name='button_box']" position="inside">
                <button name="action_import_packing_list" type="object" class="oe_stat_button" icon="fa-upload"
                        invisible="not has_marble_products or state not in ['purchase', 'done']">
                    <div class="o_field_widget o_stat_info">
                        <span class="o_stat_text">Importar</span>
                        <span class="o_stat_text">Packing List</span>
                    </div>
                </button>
                <button name="action_view_packing_lists" type="object" class="oe_stat_button" icon="fa-list"
                        invisible="packing_list_count == 0">
                    <field name="packing_list_count" widget="statinfo" string="Packing Lists"/>
                </button>
                <button name="action_view_generated_products" type="object" class="oe_stat_button" icon="fa-cubes"
                        invisible="generated_products_count == 0">
                    <field name="generated_products_count" widget="statinfo" string="Productos Generados"/>
                </button>
            </xpath>
            <!-- Añadir resumen de mármol -->
            <xpath expr="//page[@name='purchase_delivery_invoice']" position="after">
                <page string="Resumen de Mármol" name="marble_summary" invisible="not has_marble_products">
                    <group>
                        <group string="Totales">
                            <field name="total_marble_sqm" readonly="1"/>
                            <field name="packing_list_count" readonly="1"/>
                            <field name="generated_products_count" readonly="1"/>
                        </group>
                        <group string="Estado del Proceso">
                            <field name="packing_list_imported" readonly="1"/>
                        </group>
                    </group>
                    <div class="alert alert-info" role="alert" invisible="packing_list_imported">
                        <h4>📋 Siguiente Paso: Importar Packing List</h4>
                        <p>
                            Una vez confirmada la orden de compra, use el botón 
                            <strong>"Importar Packing List"</strong> para cargar 
                            los datos específicos de cada placa de mármol.
                        </p>
                    </div>
                    <div class="alert alert-success" role="alert" invisible="not packing_list_imported">
                        <h4>✅ Packing List Importado</h4>
                        <p>
                            Los productos únicos de mármol han sido generados.
                            Use los botones estadísticos para ver los detalles.
                        </p>
                    </div>
                </page>
            </xpath>
        </field>
    </record>

    <!-- Vista de lista de líneas de orden de compra -->
    <record id="purchase_order_line_list_view_marble" model="ir.ui.view">
        <field name="name">purchase.order.line.list.marble</field>
        <field name="model">purchase.order.line</field>
        <field name="inherit_id" ref="purchase.purchase_order_line_tree"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='product_qty']" position="after">
                <field name="marble_height" optional="hide" invisible="not is_marble_template"/>
                <field name="marble_width" optional="hide" invisible="not is_marble_template"/>
                <field name="marble_thickness" optional="hide" invisible="not is_marble_template"/>
                <field name="marble_custom_lot" optional="hide" invisible="not is_marble_template"/>
                <field name="marble_finish" optional="hide" invisible="not is_marble_template"/>
                <field name="estimated_pieces" optional="hide" invisible="not is_marble_template"/>
                <field name="avg_sqm_per_piece" optional="hide" invisible="not is_marble_template"/>
            </xpath>
            <xpath expr="//field[@name='product_qty']" position="before">
                <field name="is_marble_template" invisible="1"/>
            </xpath>
        </field>
    </record>

    <!-- Vista de lista de órdenes de compra con información de mármol -->
    <record id="purchase_order_list_view_marble" model="ir.ui.view">
        <field name="name">purchase.order.list.marble</field>
        <field name="model">purchase.order</field>
        <field name="inherit_id" ref="purchase.purchase_order_view_tree"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='amount_total']" position="after">
                <field name="has_marble_products" optional="hide"/>
                <field name="container_number" optional="hide" invisible="not has_marble_products"/>
                <field name="packing_list_imported" optional="hide" invisible="not has_marble_products"/>
                <field name="total_marble_sqm" optional="hide" invisible="not has_marble_products"/>
            </xpath>
        </field>
    </record>

    <!-- Vista kanban SIMPLIFICADA para órdenes de compra de mármol -->
    <record id="purchase_order_kanban_view_marble" model="ir.ui.view">
        <field name="name">purchase.order.kanban.marble</field>
        <field name="model">purchase.order</field>
        <field name="arch" type="xml">
            <kanban>
                <field name="has_marble_products"/>
                <field name="container_number"/>
                <field name="total_marble_sqm"/>
                <field name="packing_list_imported"/>
                <field name="state"/>
                <field name="partner_id"/>
                <field name="amount_total"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_global_click">
                            <div class="oe_kanban_details">
                                <strong class="o_kanban_record_title">
                                    <field name="name"/>
                                </strong>
                                <div class="o_kanban_record_subtitle">
                                    <field name="partner_id"/>
                                </div>
                                <div t-if="record.has_marble_products.raw_value" class="o_marble_order_badge">
                                    <span class="badge badge-info">Orden Mármol</span>
                                </div>
                                <div t-if="record.has_marble_products.raw_value and record.container_number.value" class="text-muted">
                                    Contenedor: <t t-esc="record.container_number.value"/>
                                </div>
                                <div t-if="record.has_marble_products.raw_value and record.total_marble_sqm.value" class="text-muted">
                                    Total: <t t-esc="record.total_marble_sqm.value"/> m²
                                </div>
                                <div t-if="record.has_marble_products.raw_value" class="text-muted">
                                    <span t-if="record.packing_list_imported.raw_value" class="text-success">
                                        ✅ Packing List Importado
                                    </span>
                                    <span t-else="" class="text-warning">
                                        ⏳ Pendiente Packing List
                                    </span>
                                </div>
                                <div class="o_kanban_record_bottom">
                                    <div class="oe_kanban_bottom_left">
                                        <field name="amount_total" widget="monetary"/>
                                    </div>
                                    <div class="oe_kanban_bottom_right">
                                        <field name="state" widget="label_selection" options="{'classes': {'draft': 'default', 'sent': 'default', 'to approve': 'warning', 'purchase': 'success', 'done': 'success', 'cancel': 'danger'}}"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Filtros de búsqueda para órdenes con mármol -->
    <record id="purchase_order_search_view_marble" model="ir.ui.view">
        <field name="name">purchase.order.search.marble</field>
        <field name="model">purchase.order</field>
        <field name="inherit_id" ref="purchase.view_purchase_order_filter"/>
        <field name="arch" type="xml">
            <xpath expr="//filter[@name='approved']" position="after">
                <separator/>
                <filter string="Órdenes con Mármol" name="marble_orders" domain="[('has_marble_products', '=', True)]"/>
                <filter string="Packing List Pendiente" name="packing_pending" domain="[('has_marble_products', '=', True), ('packing_list_imported', '=', False)]"/>
                <filter string="Packing List Importado" name="packing_imported" domain="[('has_marble_products', '=', True), ('packing_list_imported', '=', True)]"/>
                <filter string="Con Contenedor" name="with_container" domain="[('has_marble_products', '=', True), ('container_number', '!=', False)]"/>
            </xpath>
            <xpath expr="//group/filter[@name='vendor']" position="after">
                <separator/>
                <filter string="Estado Packing List" name="group_packing_status"
                    context="{'group_by': 'packing_list_imported'}"
                    domain="[('has_marble_products', '=', True)]"/>
                <filter string="Proveedor (Mármol)" name="group_marble_supplier"
                    context="{'group_by': 'partner_id'}"
                    domain="[('has_marble_products', '=', True)]"/>
            </xpath>
            <xpath expr="//field[@name='name']" position="after">
                <field name="container_number"/>
                <field name="commercial_invoice"/>
            </xpath>
        </field>
    </record>

    <!-- Acción para órdenes de compra de mármol -->
    <record id="action_purchase_order_marble" model="ir.actions.act_window">
        <field name="name">Órdenes de Compra - Mármol</field>
        <field name="res_model">purchase.order</field>
        <field name="view_mode">kanban,list,form</field>
        <field name="domain">[('has_marble_products', '=', True)]</field>
        <field name="view_id" ref="purchase_order_kanban_view_marble"/>
        <field name="context">{'search_default_marble_orders': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una nueva orden de compra de mármol
            </p>
            <p>
                Las órdenes de compra de mármol permiten gestionar la importación
                de productos desde packing lists del proveedor.
                <br/>
                <strong>Proceso:</strong>
                <br/>
                1. Crear orden con plantillas de mármol
                <br/>
                2. Confirmar la orden
                <br/>
                3. Importar packing list con datos específicos
                <br/>
                4. Productos únicos se generan automáticamente
            </p>
        </field>
    </record>

    <!-- Acción para órdenes pendientes de packing list -->
    <record id="action_purchase_order_marble_pending" model="ir.actions.act_window">
        <field name="name">Órdenes Pendientes - Packing List</field>
        <field name="res_model">purchase.order</field>
        <field name="view_mode">list,form</field>
        <field name="domain">[('has_marble_products', '=', True), ('packing_list_imported', '=', False), ('state', 'in', ['purchase', 'done'])]</field>
        <field name="context">{'search_default_packing_pending': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                No hay órdenes pendientes de packing list
            </p>
            <p>
                Aquí se muestran las órdenes de mármol confirmadas que 
                aún no tienen su packing list importado.
            </p>
        </field>
    </record>

</odoo>
```

-e ### ./wizard/packing_list_import_wizard.py
```
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import base64
import io
import csv
import json
import logging

_logger = logging.getLogger(__name__)


class PackingListImportWizard(models.TransientModel):
    _name = 'packing.list.import.wizard'
    _description = 'Wizard para Importar Packing List'
    
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Orden de Compra',
        required=True,
        readonly=True
    )
    
    container_number = fields.Char(
        string='Número de Contenedor',
        required=True
    )
    
    commercial_invoice = fields.Char(
        string='Factura Comercial',
        required=True
    )
    
    packing_list_name = fields.Char(
        string='Nombre del Packing List',
        help='Nombre descriptivo para identificar este packing list'
    )
    
    import_method = fields.Selection([
        ('csv', 'Archivo CSV'),
        ('manual', 'Entrada Manual'),
        ('excel', 'Archivo Excel')
    ], string='Método de Importación', default='csv', required=True)
    
    # Campos para archivo
    import_file = fields.Binary(
        string='Archivo de Importación',
        help='Archivo CSV o Excel con los datos del packing list'
    )
    
    filename = fields.Char(
        string='Nombre del Archivo'
    )
    
    # Campos para entrada manual
    manual_data = fields.Text(
        string='Datos en JSON',
        help='Datos en formato JSON para entrada manual'
    )
    
    # Configuración de importación
    has_header = fields.Boolean(
        string='Archivo tiene encabezados',
        default=True,
        help='Marcar si la primera fila contiene encabezados'
    )
    
    delimiter = fields.Selection([
        (',', 'Coma (,)'),
        (';', 'Punto y coma (;)'),
        ('	', 'Tabulador'),
        ('|', 'Pipe (|)')
    ], string='Delimitador', default=',')
    
    # Preview de datos
    preview_data = fields.Text(
        string='Vista Previa',
        readonly=True
    )
    
    # Estado del wizard
    step = fields.Selection([
        ('upload', 'Cargar Archivo'),
        ('preview', 'Vista Previa'),
        ('import', 'Importar')
    ], string='Paso', default='upload')
    
    # Mapeo de columnas
    column_mapping = fields.Text(
        string='Mapeo de Columnas',
        help='Mapeo de columnas en formato JSON'
    )
    
    @api.onchange('import_file', 'filename')
    def _onchange_import_file(self):
        """Generar vista previa cuando se carga un archivo"""
        if self.import_file and self.import_method in ['csv', 'excel']:
            try:
                preview = self._generate_preview()
                self.preview_data = preview
                if preview:
                    self.step = 'preview'
            except Exception as e:
                self.preview_data = f"Error al procesar archivo: {str(e)}"
    
    def _generate_preview(self):
        """Generar vista previa del archivo"""
        if not self.import_file:
            return ""
        
        try:
            file_content = base64.b64decode(self.import_file)
            
            if self.import_method == 'csv':
                return self._preview_csv(file_content)
            elif self.import_method == 'excel':
                return self._preview_excel(file_content)
                
        except Exception as e:
            return f"Error: {str(e)}"
        
        return ""
    
    def _preview_csv(self, file_content):
        """Vista previa de archivo CSV"""
        try:
            file_text = file_content.decode('utf-8')
            lines = file_text.split('
')[:10]  # Primeras 10 líneas
            
            preview = "Vista previa (primeras 10 líneas):

"
            for i, line in enumerate(lines, 1):
                if line.strip():
                    preview += f"{i:2d}: {line[:100]}...
" if len(line) > 100 else f"{i:2d}: {line}
"
            
            return preview
            
        except UnicodeDecodeError:
            try:
                file_text = file_content.decode('latin-1')
                lines = file_text.split('
')[:5]
                preview = "Vista previa (encoding latin-1):

"
                for i, line in enumerate(lines, 1):
                    if line.strip():
                        preview += f"{i}: {line[:100]}...
" if len(line) > 100 else f"{i}: {line}
"
                return preview
            except:
                return "Error: No se pudo decodificar el archivo. Verifique el encoding."
    
    def _preview_excel(self, file_content):
        """Vista previa de archivo Excel"""
        try:
            # Aquí se implementaría la lectura de Excel con openpyxl o xlrd
            return "Vista previa de Excel no implementada aún. Use CSV por favor."
        except Exception as e:
            return f"Error leyendo Excel: {str(e)}"
    
    def action_import_packing_list(self):
        """Procesar la importación del packing list"""
        self.ensure_one()
        
        if self.import_method == 'csv':
            return self._import_from_csv()
        elif self.import_method == 'manual':
            return self._import_from_manual()
        elif self.import_method == 'excel':
            return self._import_from_excel()
        else:
            raise UserError("Método de importación no soportado.")
    
    def _import_from_csv(self):
        """Importar desde archivo CSV"""
        if not self.import_file:
            raise ValidationError("Por favor, seleccione un archivo CSV.")
        
        try:
            # Decodificar archivo
            file_content = base64.b64decode(self.import_file)
            
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            file_text = None
            
            for encoding in encodings:
                try:
                    file_text = file_content.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if file_text is None:
                raise ValidationError("No se pudo decodificar el archivo. Verifique el formato.")
            
            # Configurar CSV reader
            csv_reader = csv.DictReader(
                io.StringIO(file_text),
                delimiter=self.delimiter
            )
            
            # Crear registro de importación
            packing_list_name = self.packing_list_name or f'Packing List - {self.purchase_order_id.name}'
            
            packing_list = self.env['packing.list.import'].create({
                'name': packing_list_name,
                'purchase_order_id': self.purchase_order_id.id,
                'container_number': self.container_number,
                'commercial_invoice': self.commercial_invoice,
                'state': 'draft',
                'import_date': fields.Datetime.now(),
            })
            
            # Procesar líneas
            lines_data = []
            line_count = 0
            errors = []
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start=2 porque la primera es header
                try:
                    line_data = self._process_csv_row(row, row_num)
                    if line_data:
                        line_data['packing_list_id'] = packing_list.id
                        lines_data.append(line_data)
                        line_count += 1
                except Exception as e:
                    errors.append(f"Línea {row_num}: {str(e)}")
            
            if not lines_data:
                raise ValidationError("No se encontraron datos válidos para importar.")
            
            # Crear líneas
            self.env['packing.list.import.line'].create(lines_data)
            
            # Actualizar estado
            packing_list.state = 'imported'
            
            # Preparar mensaje de resultado
            message = f"Importación completada:
"
            message += f"- {line_count} líneas importadas
"
            if errors:
                message += f"- {len(errors)} errores encontrados
"
                message += "
Errores:
" + "
".join(errors[:10])  # Mostrar solo los primeros 10
            
            # Retornar vista del packing list
            return {
                'type': 'ir.actions.act_window',
                'name': 'Packing List Importado',
                'res_model': 'packing.list.import',
                'res_id': packing_list.id,
                'view_mode': 'form',
                'target': 'current',
                'context': {
                    'form_view_initial_mode': 'edit',
                    'import_message': message
                }
            }
            
        except Exception as e:
            raise ValidationError(f"Error al procesar el archivo CSV: {str(e)}")
    
    def _process_csv_row(self, row, row_num):
        """
        Procesar una fila del CSV
        
        Formato esperado (ajustable):
        - product_name: Nombre del material
        - height: Alto en cm
        - width: Ancho en cm  
        - thickness: Grosor en cm
        - lot: Lote personalizado
        - wooden_crate: Código de atado/wooden crate
        - supplier_lot: Número de lote del proveedor
        - cost: Costo unitario
        - price_per_sqm: Precio por m²
        - finish: Acabado (opcional)
        """
        try:
            # Limpiar y validar datos
            product_name = self._clean_field(row.get('product_name') or row.get('Product Name') or row.get('Material'), 'product_name', row_num)
            height = self._parse_float(row.get('height') or row.get('Height') or row.get('Alto'), 'height', row_num)
            width = self._parse_float(row.get('width') or row.get('Width') or row.get('Ancho'), 'width', row_num)
            thickness = self._parse_float(row.get('thickness') or row.get('Thickness') or row.get('Grosor'), 'thickness', row_num)
            lot = self._clean_field(row.get('lot') or row.get('Lot') or row.get('Lote'), 'lot', row_num)
            wooden_crate = self._clean_field(row.get('wooden_crate') or row.get('Wooden Crate') or row.get('Crate'), 'wooden_crate', row_num)
            supplier_lot = self._clean_field(row.get('supplier_lot') or row.get('Supplier Lot') or row.get('Lot Number'), 'supplier_lot', row_num)
            
            # Campos opcionales
            cost = self._parse_float(row.get('cost') or row.get('Cost') or row.get('Costo'), 'cost', row_num, required=False)
            price_per_sqm = self._parse_float(row.get('price_per_sqm') or row.get('Price per SQM'), 'price_per_sqm', row_num, required=False)
            finish = self._clean_field(row.get('finish') or row.get('Finish') or row.get('Acabado'), 'finish', row_num, required=False)
            
            return {
                'product_name': product_name,
                'marble_height': height,
                'marble_width': width,
                'marble_thickness': thickness,
                'marble_custom_lot': lot,
                'wooden_crate_code': wooden_crate,
                'supplier_lot_number': supplier_lot,
                'cost_price': cost or 0.0,
                'price_per_sqm': price_per_sqm or 0.0,
                'marble_finish': finish or '',
            }
            
        except ValueError as e:
            raise ValidationError(f"Error en formato de datos: {str(e)}")
    
    def _clean_field(self, value, field_name, row_num, required=True):
        """Limpiar y validar campo de texto"""
        if not value or str(value).strip() == '':
            if required:
                raise ValueError(f"Campo requerido '{field_name}' vacío en línea {row_num}")
            return ''
        return str(value).strip()
    
    def _parse_float(self, value, field_name, row_num, required=True):
        """Parsear y validar campo numérico"""
        if not value or str(value).strip() == '':
            if required:
                raise ValueError(f"Campo numérico requerido '{field_name}' vacío en línea {row_num}")
            return 0.0
        
        try:
            # Limpiar el valor (remover espacios, comas como separadores de miles)
            clean_value = str(value).strip().replace(',', '')
            return float(clean_value)
        except (ValueError, TypeError):
            raise ValueError(f"Valor inválido para '{field_name}' en línea {row_num}: '{value}'")
    
    def _import_from_excel(self):
        """Importar desde archivo Excel"""
        raise UserError("Importación desde Excel no implementada aún. Use CSV por favor.")
    
    def _import_from_manual(self):
        """Importar desde datos manuales en JSON"""
        if not self.manual_data:
            raise ValidationError("Por favor, ingrese los datos manuales en formato JSON.")
        
        try:
            data = json.loads(self.manual_data)
            
            if not isinstance(data, list):
                raise ValidationError("Los datos deben ser una lista de objetos JSON.")
            
            # Crear registro de importación
            packing_list_name = self.packing_list_name or f'Packing List Manual - {self.purchase_order_id.name}'
            
            packing_list = self.env['packing.list.import'].create({
                'name': packing_list_name,
                'purchase_order_id': self.purchase_order_id.id,
                'container_number': self.container_number,
                'commercial_invoice': self.commercial_invoice,
                'state': 'draft',
                'import_date': fields.Datetime.now(),
            })
            
            # Procesar líneas
            lines_data = []
            for i, item in enumerate(data, 1):
                try:
                    line_data = self._process_manual_item(item, i)
                    line_data['packing_list_id'] = packing_list.id
                    lines_data.append(line_data)
                except Exception as e:
                    raise ValidationError(f"Error en elemento {i}: {str(e)}")
            
            # Crear líneas
            self.env['packing.list.import.line'].create(lines_data)
            
            # Actualizar estado
            packing_list.state = 'imported'
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Packing List Importado',
                'res_model': 'packing.list.import',
                'res_id': packing_list.id,
                'view_mode': 'form',
                'target': 'current'
            }
            
        except json.JSONDecodeError:
            raise ValidationError("Error en formato JSON. Verifique la sintaxis.")
        except Exception as e:
            raise ValidationError(f"Error al procesar los datos manuales: {str(e)}")
    
    def _process_manual_item(self, item, item_num):
        """Procesar un elemento JSON manual"""
        required_fields = ['product_name', 'marble_height', 'marble_width', 'marble_thickness', 
                          'marble_custom_lot', 'wooden_crate_code', 'supplier_lot_number']
        
        # Validar campos requeridos
        for field in required_fields:
            if field not in item or not item[field]:
                raise ValueError(f"Campo requerido '{field}' faltante o vacío")
        
        # Validar tipos de datos
        numeric_fields = ['marble_height', 'marble_width', 'marble_thickness', 'cost_price', 'price_per_sqm']
        for field in numeric_fields:
            if field in item and item[field] is not None:
                try:
                    item[field] = float(item[field])
                except (ValueError, TypeError):
                    raise ValueError(f"Valor inválido para campo numérico '{field}': {item[field]}")
        
        return item
    
    def action_generate_template(self):
        """Generar archivo CSV de plantilla"""
        self.ensure_one()
        
        # Crear CSV de ejemplo
        csv_content = '''product_name,height,width,thickness,lot,wooden_crate,supplier_lot,cost,price_per_sqm,finish
Amazon-2cm-Leather,320.5,160.2,2.0,BD00172535,BD00172535,204952-031,150.00,75.00,Leather
Metalicus-2cm-Polished,305.0,155.8,2.0,BD00172535,BD00172535,204952-032,180.00,90.00,Polished
Carrara-3cm-Honed,280.3,140.6,3.0,BD00173210,BD00173210,205464-019,200.00,66.67,Honed'''
        
        # Codificar a base64
        csv_encoded = base64.b64encode(csv_content.encode('utf-8'))
        
        # Crear attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'packing_list_template.csv',
            'type': 'binary',
            'datas': csv_encoded,
            'mimetype': 'text/csv',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
    
    def action_show_json_example(self):
        """Mostrar ejemplo de formato JSON"""
        json_example = '''[
    {
        "product_name": "Amazon-2cm-Leather",
        "marble_height": 320.5,
        "marble_width": 160.2,
        "marble_thickness": 2.0,
        "marble_custom_lot": "BD00172535",
        "wooden_crate_code": "BD00172535",
        "supplier_lot_number": "204952-031",
        "cost_price": 150.00,
        "price_per_sqm": 75.00,
        "marble_finish": "Leather"
    },
    {
        "product_name": "Metalicus-2cm-Polished",
        "marble_height": 305.0,
        "marble_width": 155.8,
        "marble_thickness": 2.0,
        "marble_custom_lot": "BD00172535", 
        "wooden_crate_code": "BD00172535",
        "supplier_lot_number": "204952-032",
        "cost_price": 180.00,
        "price_per_sqm": 90.00,
        "marble_finish": "Polished"
    }
]'''
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ejemplo de Formato JSON',
            'res_model': 'packing.list.import.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_manual_data': json_example,
                'show_json_example': True
            }
        }
```

### __init__.py
```python
# -*- coding: utf-8 -*-

from . import models
from . import wizard
```

### __manifest__.py
```python
# -*- coding: utf-8 -*-
{
    'name': 'Marble Product Base Management',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Sistema de gestión de inventario para productos de mármol con seguimiento por pieza única',
    'description': '''
        Módulo base para la gestión avanzada de inventario de productos de mármol.
        
        Características principales:
        - Creación automática de productos únicos por placa
        - Importación masiva desde Packing Lists
        - Seguimiento por número de serie único
        - Gestión de lotes personalizados
        - Integración completa con compras y inventario
        - Trazabilidad completa desde proveedor hasta venta
        
        Este módulo permite manejar cada placa de mármol como un producto único
        con sus propias dimensiones, costos y características específicas.
    ''',
    'author': 'Tu Nombre/Empresa',
    'website': 'https://tuempresa.com',
    'depends': [
        'base',
        'product',
        'stock',
        'purchase',
        'purchase_stock',
        'uom',
        'web',
        'mail', 
    ],
    'data': [
        # Seguridad
        'security/ir.model.access.csv',
        
        # Datos base
        'data/ir_sequence_data.xml',
        'data/product_uom_data.xml',
        
        # Vistas - orden corregido
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/packing_list_import_views.xml',
        'views/packing_list_import_wizard_views.xml',
        'views/purchase_order_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/product_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'marble_product_base/static/src/css/marble_styles.css',
        ],
    },
    'external_dependencies': {
        'python': [],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'sequence': 10,
    # 'images': ['static/description/icon.png'],
}
```

