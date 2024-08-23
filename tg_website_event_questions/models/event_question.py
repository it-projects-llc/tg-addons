from odoo import fields, models


class EventQuestion(models.Model):
    _inherit = "event.question"

    is_marketing = fields.Boolean()

    def _was_answered_by(self, partner):
        return partner.mapped("marketing_answers.question_id") & self


class EventQuestionAnswer(models.Model):
    _inherit = "event.question.answer"

    is_custom = fields.Boolean()
