from odoo import models


class Partner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        if not self.env.context.get("allow_attendee_partner_change"):
            self = self.with_context(partner_event_merging=True)

        return super().write(vals)
