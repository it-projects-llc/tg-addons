from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    hex_barcode = fields.Boolean("HEX Barcode")
