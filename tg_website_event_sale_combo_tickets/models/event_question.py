from odoo import api, fields, models


class EventQuestion(models.Model):
    _inherit = "event.question"

    is_shuttle_ticket = fields.Boolean(
        compute="_compute_is_shuttle_ticket", store=True, readonly=False
    )

    @api.depends("question_type")
    def _compute_is_shuttle_ticket(self):
        for record in self:
            if record.question_type != "simple_choice":
                record.is_shuttle_ticket = False

    def action_generate_shuttle_ticket_answers(self):
        w = self.env["generate.shuttle.ticket.answers"].create(
            {
                "question": self.id,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": w._name,
            "res_id": w.id,
            "view_mode": "form",
            "target": "new",
        }
