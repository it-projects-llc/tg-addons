from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_hex_barcode = fields.Boolean(
        related="pos_config_id.hex_barcode",
        readonly=False,
    )
