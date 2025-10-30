from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GenerateShuttleTicketAnswers(models.TransientModel):
    _name = "generate.shuttle.ticket.answers"
    _description = "Generate Shuttle Ticket Answers"

    question = fields.Many2one("event.question", required=True, readonly=True)
    events_to_generate_from = fields.Many2many("event.event")
    events_to_generate_from_domain = fields.Binary(compute="_compute_domain")

    @api.depends("question")
    def _compute_domain(self):
        for w in self:
            w.events_to_generate_from_domain = [
                ("stage_id.pipe_end", "=", False),
                ("id", "!=", w.question.event_id.id),
            ]

    def generate(self):
        EQA = self.env["event.question.answer"].sudo()
        for w in self:
            shuttle_events = w.events_to_generate_from
            if not shuttle_events:
                raise UserError(_("Shuttle events are not chosen"))

            existing_answers = w.question.answer_ids
            for event, ticket in self._fetch_tickets_from_events(
                shuttle_events
            ).items():
                answer = existing_answers.filtered(lambda x: x.shuttle_ticket == ticket)  # noqa: B023
                if answer:
                    answer.name = self._prepare_answer(event)

                else:
                    answer = EQA.create(
                        {
                            "name": self._prepare_answer(event),
                            "question_id": w.question.id,
                            "shuttle_ticket": ticket.id,
                        }
                    )

            sorted_answers = w.question.answer_ids.filtered("shuttle_ticket").sorted(
                lambda x: x.shuttle_ticket.event_id.date_begin
            )
            for c, a in enumerate(sorted_answers):
                a.sequence = c * 10

    @api.model
    def _prepare_answer(self, event):
        return event.date_begin_located

    @api.model
    def _fetch_tickets_from_events(self, events):
        res = {}
        tickets = self.env["event.event.ticket"].search(
            [
                ("event_id", "in", events.ids),
            ],
            order="price ASC",
        )
        for t in tickets:
            res[t.event_id] = t
        return res
