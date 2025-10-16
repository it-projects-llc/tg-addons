from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    accomodation_category = fields.Many2one(
        "product.public.category", config_parameter="tg.accomodation_category"
    )
