from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    tnc_url = fields.Char("TNC URL")
    tnc_title = fields.Char("TNC Title")
