from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    tnc_accepted = fields.Boolean("Accepted TNC")
