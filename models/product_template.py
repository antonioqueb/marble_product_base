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
    
    # ✅ NUEVOS CAMPOS para la solución
    is_generated_marble_template = fields.Boolean(
        string='Plantilla de Mármol Generada',
        default=False,
        help='Indica si esta plantilla fue generada automáticamente para una placa única.'
    )

    marble_prototype_template_id = fields.Many2one(
        'product.template',
        string='Plantilla Prototipo',
        help='La plantilla base desde la cual se generó esta plantilla única.'
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
                # ✅ ACTUALIZACIÓN: Contar plantillas generadas en lugar de productos
                generated_templates = self.env['product.template'].search_count([
                    ('marble_prototype_template_id', '=', record.id)
                ])
                record.generated_products_count = generated_templates
            else:
                record.generated_products_count = 0
    
    @api.onchange('is_marble_template')
    def _onchange_is_marble_template(self):
        """Configurar valores por defecto para plantillas de mármol"""
        if self.is_marble_template:
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
        
        # ✅ ACTUALIZACIÓN: Buscar plantillas generadas en lugar de productos directos
        generated_templates = self.env['product.template'].search([
            ('marble_prototype_template_id', '=', self.id)
        ])
        
        # Obtener los products de estas plantillas
        generated_products = self.env['product.product'].search([
            ('product_tmpl_id', 'in', generated_templates.ids)
        ])
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Productos Generados - %s') % self.name,
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', generated_products.ids)],
            'context': {
                'create': False,
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