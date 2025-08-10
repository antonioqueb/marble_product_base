# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StockLot(models.Model):
    _inherit = ['stock.lot', 'mail.thread', 'mail.activity.mixin']

    marble_tone = fields.Char(string='Tono')
    marble_vein = fields.Char(string='Veta')
    marble_density = fields.Float(string='Densidad', help='Densidad del material (kg/m³)')
    marble_weight = fields.Float(string='Peso', compute='_compute_weight', store=True)
    defectos_observaciones = fields.Text(string='Defectos / Observaciones')
    image_ids = fields.Many2many('ir.attachment', 'lot_image_rel', 'lot_id', 'attachment_id', string='Fotos')

    @api.depends('product_id', 'marble_density')
    def _compute_weight(self):
        for lot in self:
            volume = 0.0
            product = lot.product_id
            if product.marble_height and product.marble_width and product.marble_thickness:
                volume = (product.marble_height / 100) * (product.marble_width / 100) * (product.marble_thickness / 100)
            lot.marble_weight = lot.marble_density * volume if lot.marble_density and volume else 0.0
