from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    affilation_tag = fields.Many2one(
        "event.tag", config_parameter="tg_website_event_sale.affilation_tag"
    )
