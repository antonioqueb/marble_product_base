# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MarbleTaxonomy(models.Model):
    _name = 'marble.taxonomy'
    _description = 'Taxonomía Mármol'

    name = fields.Char(required=True)
    parent_id = fields.Many2one('marble.taxonomy', string='Padre')
    child_ids = fields.One2many('marble.taxonomy', 'parent_id', string='Hijos')
    level = fields.Selection([
        ('family', 'Familia'),
        ('material', 'Material'),
        ('format', 'Formato'),
        ('thickness', 'Espesor'),
        ('finish', 'Acabado'),
        ('color', 'Color/Tono'),
    ], required=True)

    _sql_constraints = [
        ('name_level_unique', 'unique(name, level, parent_id)', 'Valor duplicado en la taxonomía.')
    ]

    @api.constrains('parent_id')
    def _check_parent_level(self):
        for rec in self:
            if rec.parent_id and rec.level and rec.parent_id.level:
                order = ['family', 'material', 'format', 'thickness', 'finish', 'color']
                if order.index(rec.level) <= order.index(rec.parent_id.level):
                    raise ValidationError(_('Nivel jerárquico incorrecto para %s') % rec.name)
