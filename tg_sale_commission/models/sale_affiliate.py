from odoo import fields, models


class SaleAffiliate(models.Model):
    _inherit = "sale.affiliate"

    partner_id = fields.Many2one("res.partner", domain="[('agent', '=', True)]")
