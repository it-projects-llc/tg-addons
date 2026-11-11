from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_max_split_orders = fields.Integer(related="pos_config_id.pos_max_split_orders", readonly=False)
