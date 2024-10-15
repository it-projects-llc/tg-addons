from odoo import fields, models
from odoo.tools import DotDict


class Partner(models.Model):
    _inherit = "res.partner"

    marketing_1 = fields.Many2one(
        "res.partner.marketing.answer", string="How did you find about us?"
    )

    def _get_unanswered_marketing_questions(self):
        self.ensure_one()
        Fields = self.sudo().env["ir.model.fields"]
        MarketingAnswers = self.sudo().env["res.partner.marketing.answer"]

        marketing_fields = Fields.search(
            [
                ("model", "=", self._name),
                ("name", "like", "marketing_"),
            ]
        )

        res = []
        for field in marketing_fields:
            fname = field.name
            if self[fname]:
                continue

            canned_answers = MarketingAnswers.search(
                [
                    ("field", "=", field.id),
                    ("is_canned", "=", True),
                ]
            )

            res.append(
                DotDict(
                    {
                        "title": self._fields[fname]._description_string(self.env),
                        "field_name": field.name,
                        "canned_answers": canned_answers,
                    }
                )
            )

        return res
