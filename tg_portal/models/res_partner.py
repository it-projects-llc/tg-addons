from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    is_passport_not_ready = fields.Boolean()
