from odoo import api, fields, models


class EventTemplateTicket(models.Model):
    _inherit = "event.type.ticket"

    include_accomodation = fields.Boolean("Navigate to accomodation")


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    @api.depends_context("name_with_event_name")
    def _compute_display_name(self):
        if not self.env.context.get("name_with_event_name"):
            return super()._compute_display_name()

        for ticket in self:
            event = ticket.event_id
            ticket.display_name = f"{ticket.name} ({event.name})"
