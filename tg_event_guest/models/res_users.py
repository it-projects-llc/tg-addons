from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    event_guest = fields.Many2one("event.guest", compute="_compute_event_guest")

    def _compute_event_guest(self):
        event_guests = self.env["event.guest"].search(
            [
                ("result_partner", "in", self.mapped("partner_id").ids),
            ]
        )
        d = {x.result_partner.id: x.id for x in event_guests}
        for user in self:
            user.event_guest = d.get(user.partner_id.id, False)
