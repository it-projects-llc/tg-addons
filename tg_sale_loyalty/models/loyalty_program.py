from odoo import fields, models


class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    is_accumulative = fields.Boolean(
        default=True,
        help="Allows to accumulate the program with other applied loyalty programs",
    )
