from odoo import fields, models


class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    nationality_programs = fields.One2many(
        "nationality.discount.program",
        "discount_program",
        string="Apply To Nationalities",
    )
