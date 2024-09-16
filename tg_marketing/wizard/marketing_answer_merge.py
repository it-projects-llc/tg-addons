from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MarketingAnswerMerge(models.TransientModel):
    _name = "marketing.answer.merge"
    _description = "Marketing answer merge"

    @api.model
    def default_get(self, fields):
        res = super(MarketingAnswerMerge, self).default_get(fields)
        active_ids = self.env.context.get("active_ids")
        if not active_ids:
            return res

        MarketingAnswers = self.env["res.partner.marketing.answer"]
        answers = MarketingAnswers.browse(active_ids)
        question = answers.mapped("field")
        if len(question) > 1:
            raise UserError(_("Cannot merge answers with different questions"))

        if "question" in fields:
            res["question"] = question.id

        if "dst_answer" in fields:
            canned_answer = answers.filtered("is_canned")[:1]
            if canned_answer:
                res["dst_answer"] = canned_answer.id
            else:
                res["dst_answer"] = answers[:1].id

        if "answers" in fields:
            res["answers"] = [(6, 0, answers.ids)]

        return res

    question = fields.Many2one("ir.model.fields", readonly=True, required=True)
    dst_answer = fields.Many2one(
        "res.partner.marketing.answer", string="Destination answer", required=True
    )
    answers = fields.Many2many("res.partner.marketing.answer")

    def action_merge(self):
        Partner = self.with_context(active_test=False).sudo().env["res.partner"]
        for wizard in self.filtered("dst_answer"):
            fname = wizard.question.name
            answers = wizard.answers
            dst_answer = wizard.dst_answer

            partners_to_change = Partner.search(
                [
                    (fname, "in", answers.ids),
                ]
            )
            partners_to_change.write(
                {
                    fname: dst_answer.id,
                }
            )
            (answers - dst_answer).unlink()
