from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    group_name = fields.Char(
        "Group / Band Name",
        help="Specify a group the contact belongs to, e.g. band, tribe",
    )

    alias_name = fields.Char(
        "Alias / Nickname",
        help="Specify Nickname/Alias of the contact",
    )
