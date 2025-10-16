from odoo import api, fields, models


class EventQuestion(models.Model):
    _inherit = "event.question"

    is_shuttle_ticket = fields.Boolean(compute="_compute_is_shuttle_ticket", store=True)

    @api.depends("question_type")
    def _compute_is_shuttle_ticket(self):
        for record in self:
            if record.question_type != "simple_choice":
                record.is_shuttle_ticket = False
