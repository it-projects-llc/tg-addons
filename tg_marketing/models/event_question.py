from odoo import api, fields, models


class EventQuestion(models.Model):
    _inherit = "event.question"

    is_marketing = fields.Boolean(compute="_compute_is_marketing")

    @api.depends("partner_field_type", "partner_field_name")
    def _compute_is_marketing(self):
        for question in self:
            if (
                question.question_type == "partner_field"
                and question.partner_field_type == "many2one"
                and question.partner_field_name.startswith("marketing_")
            ):
                question.is_marketing = True
            else:
                question.is_marketing = False

    def get_select_options(self):
        self.ensure_one()

        if not self.is_marketing:
            return super().get_select_options()

        MarketingAnswers = self.sudo().env["res.partner.marketing.answer"]

        canned_answers = MarketingAnswers.search(
            [
                ("field", "=", self.partner_field.id),
                ("is_canned", "=", True),
            ]
        )

        return [{"id": r.id, "name": r.answer} for r in canned_answers]

    def _should_be_shown(self):
        if not self.is_marketing:
            # not our case
            return True

        user = self.env.user
        if user._is_public():
            # do not show marketing question to public user
            return False

        partner = user.partner_id
        if partner[self.partner_field_name]:
            # marketing field is already set
            return False

        return True

    def _parse_partner_field_answer(self, answer):
        if not self.is_marketing:
            return super()._parse_partner_field_answer(answer)

        MarketingAnswers = self.sudo().env["res.partner.marketing.answer"]
        value = answer["value_text_box"]
        field = self.sudo().partner_field

        try:
            answer_id = int(value)
            answer_record = MarketingAnswers.browse(answer_id).exists()
            if not answer_record:
                raise ValueError()
            if answer_record.field.id != field.id:
                raise ValueError()

            answer["value_text_box"] = answer_record.answer
            return answer_id

        except (IndexError, ValueError):
            answer_record = MarketingAnswers.search(
                [("field", "=", field.id), ("answer", "=", value)], limit=1
            )
            if not answer_record:
                answer_record = MarketingAnswers._create_custom_answer(field, value)

            return answer_record.id
