from odoo import api, fields, models


class EventQuestionAnswer(models.Model):
    _inherit = "event.question.answer"

    shuttle_ticket = fields.Many2one("event.event.ticket")
    shuttle_ticket_domain = fields.Binary(compute="_compute_shuttle_ticket_domain")

    @api.depends("question_id.event_id")
    def _compute_shuttle_ticket_domain(self):
        for record in self:
            if record.question_id.event_id:
                record.shuttle_ticket_domain = [
                    ("event_id.event_registrations_open", "=", True)
                ]
            else:
                record.shuttle_ticket_domain = [(1, "=", 0)]
