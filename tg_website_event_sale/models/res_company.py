from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    affilation_tag = fields.Many2one("event.tag")
