from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_shop_ref_id = fields.Many2one(
        related="pos_config_id.shop_ref_id", readonly=False
    )
