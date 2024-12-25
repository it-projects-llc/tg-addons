from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    subscribe_in_registrations = fields.Many2many(
        "res.partner", "event_reg_sub_partner"
    )
    default_email_template_id = fields.Many2one(
        "mail.template",
        domain="[('model', '=', 'event.registration')]",
        help="Default email template used upon manual sending the emails to attendees using "
        "Send By Email button in the event registration form",
    )
