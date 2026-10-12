from odoo import fields, models

class PosConfig(models.Model):
    _inherit = "pos.config"

    pos_max_split_orders = fields.Integer("Max Orders to Split", default=3)
