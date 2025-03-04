from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    logins = fields.Char("Related User Logins", compute="_compute_logins")

    @api.depends("user_ids.login")
    def _compute_logins(self):
        for partner in self:
            partner.logins = ", ".join(partner.mapped("user_ids.login"))
