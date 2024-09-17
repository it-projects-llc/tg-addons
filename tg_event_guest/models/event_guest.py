from random import choice as random_choice
from string import ascii_lowercase, digits
from urllib.parse import urljoin

from odoo import api, fields, models


class EventGuest(models.Model):
    _name = "event.guest"
    _description = "Event Guest"
    _order = "id DESC"

    @api.model
    def _default_code(self):
        return "".join([random_choice(ascii_lowercase + digits) for i in range(8)])

    name = fields.Char(required=True)
    email = fields.Char(required=True)
    event = fields.Many2one(
        "event.event", required=True, domain="[('stage_id.pipe_end', '=', False)]"
    )
    event_ticket = fields.Many2one(
        "event.event.ticket",
        required=True,
        domain="[('event_id', '=', event), ('price', '=', 0)]",
    )
    code = fields.Char(
        index=True, required=True, default=lambda self: self._default_code()
    )

    invite_url = fields.Char("Invite URL", compute="_compute_invite_url", store=False)
    invited_by = fields.Many2one("res.partner", readonly=True)
    guest_of = fields.Many2one("res.partner")

    result_partner = fields.Many2one(
        "res.partner", string="Related partner", readonly=True
    )
    result_attendee = fields.Many2one(
        "event.registration", string="Related attendee", readonly=True
    )

    _sql_constraints = [
        (
            "code_unique",
            "unique(code)",
            "Code must be unique",
        ),
    ]

    @api.model
    def _get_by_code(self, code):
        return self.sudo().search(
            [
                ("code", "=", code),
            ],
            limit=1,
        )

    @api.depends("code", "event")
    def _compute_invite_url(self):
        for guest in self:
            guest.invite_url = urljoin(
                guest.event.get_base_url(),
                f"/web/signup?guest_register_code={guest.code}&redirect=%2Fmy%2Faccount",
            )
