from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    affilation_tag = fields.Many2one(
        related="company_id.affilation_tag",
        readonly=False,
    )
