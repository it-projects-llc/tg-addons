from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    redirect = fields.Char()
