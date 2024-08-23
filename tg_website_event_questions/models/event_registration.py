from odoo import fields, models


class EventRegistrationAnswer(models.Model):
    _inherit = "event.registration.answer"

    is_marketing_question = fields.Boolean(related="question_id.is_marketing")
