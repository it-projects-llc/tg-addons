from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    is_passport_not_ready = fields.Boolean()
