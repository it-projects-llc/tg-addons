from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model_create_multi
    def create(self, vals_list):
        records = super(EventRegistration, self).create(vals_list)
        for record in records:
            record.message_subscribe(record.event_id.subscribe_in_registrations.ids)
        return records
