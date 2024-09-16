from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    marketing_1 = fields.Many2one(
        "res.partner.marketing.answer", string="How did you find about us?"
    )
