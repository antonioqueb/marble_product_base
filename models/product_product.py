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
    
    # ✅ MANTENER NOMBRE ORIGINAL para compatibilidad con vistas existentes
    marble_parent_template_id = fields.Many2one(
        'product.template',
        string='Plantilla Prototipo',
        help='Plantilla prototipo de mármol desde la cual se generó este producto',
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
        store=True,
        help='Stock disponible actual'
    )

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
    
    # ⚠️ MÉTODO REESCRITO COMPLETAMENTE
    @api.model
    def create_marble_product_from_template(self, prototype_template_id, marble_data, packing_line_id=None):
        """
        Crea una plantilla y un producto únicos de mármol basados en una plantilla prototipo.
        
        Args:
            prototype_template_id (int): ID de la plantilla prototipo (ej. "Mármol Carrara").
            marble_data (dict): Datos específicos de la placa.
            packing_line_id (int): ID de la línea del packing list.
            
        Returns:
            product.product: El producto único (variante) creado.
        """
        PrototypeTemplate = self.env['product.template'].browse(prototype_template_id)
        
        if not PrototypeTemplate.exists() or not PrototypeTemplate.is_marble_template:
            raise ValidationError(_("La plantilla prototipo especificada no es válida."))

        # 1. Generar número de serie y nombre único
        serial_number = self._generate_marble_serial_number(
            marble_data.get('marble_custom_lot', ''),
            marble_data.get('supplier_lot_number', '')
        )
        unique_product_name = self._generate_marble_product_name(PrototypeTemplate, marble_data, serial_number)

        # 2. Copiar la plantilla prototipo para crear una plantilla única para esta placa
        new_template = PrototypeTemplate.copy({
            'name': unique_product_name,
            'is_marble_template': False,  # Ya no es una plantilla base
            'is_generated_marble_template': True, # Es una plantilla generada para una placa
            'marble_prototype_template_id': PrototypeTemplate.id,
            'marble_height': marble_data.get('marble_height'),
            'marble_width': marble_data.get('marble_width'),
            'marble_thickness': marble_data.get('marble_thickness'),
            'marble_finish': marble_data.get('marble_finish'),
            'standard_price': marble_data.get('cost_price', PrototypeTemplate.standard_price),
            'list_price': 0, # Precio de venta se manejará aparte si es necesario
            'active': True, # Asegurar que esté activa
        })

        # 3. Odoo crea automáticamente el product.product al crear el template. Lo obtenemos.
        #    Para un template sin atributos, siempre habrá una y solo una variante.
        product_variant = new_template.product_variant_id
        if not product_variant:
            # Fallback por si algo en la configuración impide la creación automática
            product_variant = self.search([('product_tmpl_id', '=', new_template.id)], limit=1)
            if not product_variant:
                 raise ValidationError(_("No se pudo crear la variante del producto para la nueva plantilla."))

        # 4. Escribir los datos específicos del product.product en la variante
        product_variant.write({
            'is_generated_marble_product': True,
            'marble_parent_template_id': PrototypeTemplate.id, # Referencia al prototipo
            'marble_serial_number': serial_number,
            'marble_status': 'draft',
            'marble_creation_date': fields.Datetime.now(),
            'packing_list_import_line_id': packing_line_id,
            'container_number': marble_data.get('container_number', ''),
            'commercial_invoice': marble_data.get('commercial_invoice', ''),
            'supplier_lot_number': marble_data.get('supplier_lot_number', ''),
            'wooden_crate_code': marble_data.get('wooden_crate_code', ''),
            'marble_custom_lot': marble_data.get('marble_custom_lot', ''),
            'tracking': 'serial', # Aseguramos el seguimiento por serie
        })
        
        # 5. Crear el Lote/Número de serie en stock.lot
        lot_vals = {
            'name': serial_number,
            'product_id': product_variant.id,
            'company_id': self.env.company.id,
        }
        self.env['stock.lot'].create(lot_vals)
        
        _logger.info(f"Producto de mármol creado: {product_variant.name} (ID: {product_variant.id}) con lote: {serial_number}")
        
        return product_variant
    
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