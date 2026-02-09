from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    renting_default_start_date = fields.Date()
    renting_default_end_date = fields.Date()
    renting_min_start_date = fields.Date()
    renting_max_end_date = fields.Date()
