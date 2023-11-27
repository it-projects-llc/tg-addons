from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    commission_settlement_company = fields.Many2one(
        "res.company", domain="[('id', '!=', id), ('currency_id', '=', currency_id)]"
    )
