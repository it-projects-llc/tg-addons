from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    is_period = fields.Boolean()
