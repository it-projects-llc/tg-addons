from odoo import api, models


class EventEvent(models.Model):
    _inherit = "event.event"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records.question_ids._check_accomodation_answers()
        return records

    def write(self, vals):
        res = super().write(vals)
        self.question_ids._check_accomodation_answers()
        return res
