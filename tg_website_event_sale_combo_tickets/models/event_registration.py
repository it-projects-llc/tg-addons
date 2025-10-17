from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    parent_reg_for_shuttle = fields.Many2one(
        "event.registration", "Parent registration for shuttle"
    )
    shuttle_regs = fields.One2many(
        "event.registration", "parent_reg_for_shuttle", "Shuttle registrations"
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._generate_shuttle_registrations()
        return records

    def write(self, vals):
        confirming = vals.get("state") in {"open", "done"}
        to_confirm = (
            self.filtered(
                lambda registration: registration.state in {"draft", "cancel"}
            )
            if confirming
            else None
        )
        res = super().write(vals)
        if confirming:
            to_confirm._generate_shuttle_registrations()

        return res

    def _generate_shuttle_registrations(self):
        to_generate = self.filtered(
            "registration_answer_choice_ids.value_answer_id.shuttle_ticket"
        )
        for parent in to_generate:
            shuttle_tickets = parent.mapped(
                "registration_answer_choice_ids.value_answer_id.shuttle_ticket"
            )
            for shuttle_ticket in shuttle_tickets:
                parent.copy(
                    {
                        "parent_reg_for_shuttle": parent.id,
                        "event_ticket_id": shuttle_ticket.id,
                        "event_id": shuttle_ticket.event_id.id,
                        "registration_answer_ids": False,
                        "registration_answer_choice_ids": False,
                        "state": "open",
                    }
                )
