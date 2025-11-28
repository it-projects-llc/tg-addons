from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    renting_default_start_date = fields.Date(
        related="company_id.renting_default_start_date", readonly=False
    )

    renting_default_end_date = fields.Date(
        related="company_id.renting_default_end_date", readonly=False
    )

    renting_min_start_date = fields.Date(
        related="company_id.renting_min_start_date", readonly=False
    )

    renting_max_end_date = fields.Date(
        related="company_id.renting_max_end_date", readonly=False
    )
