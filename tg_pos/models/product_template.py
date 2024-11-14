from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    shop_ids = fields.Many2many("pos.shop")
