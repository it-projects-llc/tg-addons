from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EventQuestion(models.Model):
    _inherit = "event.question"

    is_shuttle_ticket = fields.Boolean(
        compute="_compute_is_shuttle_ticket", store=True, readonly=False
    )

    is_accomodation = fields.Boolean(
        compute="_compute_is_accomodation", store=True, readonly=False
    )

    @api.depends("question_type")
    def _compute_is_shuttle_ticket(self):
        for record in self:
            if record.question_type != "simple_choice":
                record.is_shuttle_ticket = False

    @api.depends("question_type")
    def _compute_is_accomodation(self):
        for record in self:
            if record.question_type != "simple_choice":
                record.is_accomodation = False

    @api.constrains("is_shuttle_ticket", "is_accomodation")
    def _check_shuttle_accomodation(self):
        for record in self:
            if record.is_shuttle_ticket and record.is_accomodation:
                raise UserError(
                    _("Question cannot be both for shuttle and accomodation")
                )

    def action_generate_ticket_answers(self):
        self._check_shuttle_accomodation()

        if self.is_shuttle_ticket:
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

        elif self.is_accomodation:
            EQA = self.env["event.question.answer"].sudo()

            has_positive_accomodation_answer = any(
                self.answer_ids.is_positive_accomodation_answer
            )
            if not has_positive_accomodation_answer:
                EQA.create(
                    {
                        "name": _("Yes"),
                        "question_id": self.id,
                        "is_positive_accomodation_answer": False,
                    }
                )

        else:
            raise NotImplementedError()

    # TODO: проверка, что есть положительные ответ на accomodation question
