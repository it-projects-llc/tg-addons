from odoo import fields, models


class PosShop(models.Model):
    _name = "pos.shop"
    _description = "POS Shop"

    name = fields.Char(required=True)
    product_ids = fields.Many2many(
        "product.template",
        string="Products in Shop",
        domain=[("sale_ok", "=", True), ("available_in_pos", "=", True)],
    )
