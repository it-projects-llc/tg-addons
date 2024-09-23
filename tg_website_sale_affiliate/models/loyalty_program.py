from odoo import fields, models


class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    only_affiliate_usage = fields.Boolean()
    affiliates = fields.One2many("sale.affiliate", "code_promo_program_id")
