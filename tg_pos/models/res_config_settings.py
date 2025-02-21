from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_shop_ref_id = fields.Many2one(
        related="pos_config_id.shop_ref_id", readonly=False
    )
    pos_auto_duplicate_invoices = fields.Boolean(
        related="pos_config_id.auto_duplicate_invoices", readonly=False
    )
    pos_show_auto_duplicate_invoices = fields.Boolean(
        related="pos_config_id.show_auto_duplicate_invoices", readonly=False
    )
    pos_debug_auto_duplicate_invoices = fields.Boolean(
        related="pos_config_id.debug_auto_duplicate_invoices", readonly=False
    )
