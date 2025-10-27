from odoo import _, api, fields, models
from odoo.exceptions import UserError


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

    def _check_accomodation_category(self):
        tickets_with_accomodation = self.filtered("include_accomodation")
        if not tickets_with_accomodation:
            return

        for company in tickets_with_accomodation.mapped("event_id.company_id"):
            if not company.accomodation_category:
                raise UserError(_("Accomodation category is not set in settings"))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._check_accomodation_category()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._check_accomodation_category()
        return res
