from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def send_mail(self, *args, **kw):
        for wizard in self.filtered(lambda w: w.model == "event.guest"):
            active_ids = self.env.context.get("active_ids") or [wizard.res_id]
            self.env[wizard.model].browse(
                active_ids
            ).invited_by = self.env.user.partner_id
        return super().send_mail(*args, **kw)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if res.get("model") == "event.guest" and res.get("email_from"):
            res["reply_to"] = res["email_from"]
        return res
