from odoo import api, fields, models


class Country(models.Model):
    _inherit = "res.country"

    active = fields.Boolean(default=True)
