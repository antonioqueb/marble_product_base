from odoo import models, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_marble_template = fields.Boolean(
        string='¿Es Mármol?',
        related='product_id.is_marble_template',
        store=True,
        readonly=True
    )
