# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    # ============================================
    # CAMPOS RELACIONADOS PARA PRODUCTOS DE MÁRMOL
    # ============================================
    
    is_marble_product = fields.Boolean(
        string='Es Producto de Mármol',
        compute='_compute_is_marble_product',
        store=True,
        help='Indica si este stock es de un producto de mármol único'
    )

    @api.depends('product_id')
    def _compute_is_marble_product(self):
        """Determinar si el quant corresponde a un producto de mármol"""
        for quant in self:
            quant.is_marble_product = bool(getattr(quant.product_id, 'is_generated_marble_product', False))
    
    marble_serial_number = fields.Char(
        string='Nº Serie',
        related='product_id.marble_serial_number',
        store=True,
        readonly=True
    )
    
    marble_status = fields.Selection(
        string='Estado Mármol',
        related='product_id.marble_status',
        store=True,
        readonly=True
    )
    
    marble_height = fields.Float(
        string='Alto (cm)',
        related='product_id.marble_height',
        store=True,
        readonly=True
    )
    
    marble_width = fields.Float(
        string='Ancho (cm)',
        related='product_id.marble_width',
        store=True,
        readonly=True
    )
    
    marble_thickness = fields.Float(
        string='Grosor (cm)',
        related='product_id.marble_thickness',
        store=True,
        readonly=True
    )
    
    marble_sqm = fields.Float(
        string='M²',
        related='product_id.marble_sqm',
        store=True,
        readonly=True
    )
    
    marble_custom_lot = fields.Char(
        string='Lote',
        related='product_id.marble_custom_lot',
        store=True,
        readonly=True
    )
    
    wooden_crate_code = fields.Char(
        string='Código Atado',
        related='product_id.wooden_crate_code',
        store=True,
        readonly=True
    )
    
    marble_origin = fields.Char(
        string='Origen',
        related='product_id.marble_origin',
        store=True,
        readonly=True
    )
    
    marble_finish = fields.Char(
        string='Acabado',
        related='product_id.marble_finish',
        store=True,
        readonly=True
    )