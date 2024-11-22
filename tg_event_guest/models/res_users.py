from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    event_guest = fields.Many2one("event.guest", compute="_compute_event_guest")

    def _compute_event_guest(self):
        all_partner_ids = self.mapped("partner_id").ids
        event_guests = self.env["event.guest"].search(
            [
                "|",
                ("result_partner", "in", all_partner_ids),
                ("guest_partner", "in", all_partner_ids),
            ],
            order="id ASC",
        )
        d = {(x.result_partner or x.guest_partner).id: x.id for x in event_guests}
        for user in self:
            user.event_guest = d.get(user.partner_id.id, False)

    @api.model
    def signup(self, values, token=None):
        guest_register_code = values.pop("guest_register_code", False)
        res = super().signup(values, token)
        if guest_register_code:
            guest = self.env["event.guest"]._get_by_code(guest_register_code)
            if guest and not guest.result_partner:
                user = self.search(
                    [
                        ("login", "=", res[0]),
                    ],
                    limit=1,
                )
                guest.result_partner = user.partner_id

        return res
