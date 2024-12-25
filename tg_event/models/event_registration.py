from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model_create_multi
    def create(self, vals_list):
        records = super(EventRegistration, self).create(vals_list)
        for record in records:
            record.message_subscribe(record.event_id.subscribe_in_registrations.ids)
        return records

    # Set email template taken from the related Event as default upon manual email
    # sending to attendee in event registration form
    def action_send_badge_email(self):
        res = super(EventRegistration, self).action_send_badge_email()
        default_tmpl = self.event_id.default_email_template_id
        template = self.env["mail.template"].search([("id", "=", default_tmpl.id)])
        ctx = dict(
            default_model="event.registration",
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode="comment",
            custom_layout="mail.mail_notification_light",
        )
        res.update({"context": ctx})
        return res
