from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventQuestion(models.Model):
    _inherit = "event.question"

    is_shuttle = fields.Boolean(
        compute="_compute_is_shuttle", store=True, readonly=False
    )

    is_accomodation = fields.Boolean(
        compute="_compute_is_accomodation", store=True, readonly=False
    )

    @api.depends("question_type")
    def _compute_is_shuttle(self):
        for record in self:
            if record.question_type != "simple_choice":
                record.is_shuttle = False

    @api.depends("question_type")
    def _compute_is_accomodation(self):
        for record in self:
            if record.question_type != "simple_choice":
                record.is_accomodation = False

    @api.constrains("is_shuttle", "is_accomodation")
    def _check_shuttle_accomodation(self):
        for record in self:
            if record.is_shuttle and record.is_accomodation:
                raise ValidationError(
                    _("Question cannot be both for shuttle and accomodation")
                )

    def _check_accomodation_answers(self, allow_empty=False):
        for question in self.filtered("is_accomodation"):
            flags = question.answer_ids.mapped("is_positive_accomodation_answer")
            if not flags and allow_empty:
                continue

            has_positive_accomodation_answer = any(flags)
            if not has_positive_accomodation_answer:
                raise ValidationError(
                    _(
                        'Accomodation "%s" question should have positive answer',
                        question.title,
                    )
                )

    def _check_accomodation_category(self):
        questions = self.filtered("is_accomodation")

        for company in questions.mapped("event_id.company_id"):
            if not company.accomodation_category:
                raise ValidationError(_("Accomodation category is not set in settings"))

    def action_generate_ticket_answers(self):
        self._check_shuttle_accomodation()

        if self.is_shuttle:
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
                self.answer_ids.mapped("is_positive_accomodation_answer")
            )
            if not has_positive_accomodation_answer:
                EQA.create(
                    {
                        "name": _("Yes"),
                        "question_id": self.id,
                        "is_positive_accomodation_answer": True,
                    }
                )

        else:
            raise NotImplementedError()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._check_accomodation_category()
        records._check_accomodation_answers(allow_empty=True)
        return records

    def write(self, vals):
        res = super().write(vals)
        self._check_accomodation_category()
        self._check_accomodation_answers(allow_empty=True)
        return res
