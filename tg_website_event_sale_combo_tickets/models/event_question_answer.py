from odoo import api, fields, models


class EventQuestionAnswer(models.Model):
    _inherit = "event.question.answer"

    shuttle_ticket = fields.Many2one("event.event.ticket")
    shuttle_ticket_domain = fields.Binary(compute="_compute_shuttle_ticket_domain")
    is_positive_accomodation_answer = fields.Boolean()

    @api.depends("question_id.event_id")
    def _compute_shuttle_ticket_domain(self):
        for record in self:
            record.shuttle_ticket_domain = [
                ("event_id.stage_id.pipe_end", "=", False),
            ]

    @api.onchange("shuttle_ticket")
    def _onchange_shuttle_ticket(self):
        if not self.name and self.shuttle_ticket:
            self.name = self.shuttle_ticket.name
