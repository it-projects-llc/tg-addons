from odoo import api, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record.message_subscribe(record.event_id.subscribe_in_registrations.ids)
        return records

    # Set email template taken from the related Event as default
    # upon manual email sending in event registration form
    def action_send_badge_email(self):
        res = super().action_send_badge_email()

        default_tmpl = self.event_id.default_email_template_id
        template = self.env["mail.template"].search([("id", "=", default_tmpl.id)])
        ctx = dict(
            default_model="event.registration",
            default_res_ids=self.ids,
            default_template_id=template.id if template else False,
            default_composition_mode="comment",
            default_email_layout_xmlid="mail.mail_notification_light",
        )
        res.update({"context": ctx})
        return res
