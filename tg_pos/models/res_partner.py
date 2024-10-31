from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    barcode = fields.Char(company_dependent=False)
