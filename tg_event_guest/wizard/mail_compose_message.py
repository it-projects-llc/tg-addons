from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_send_mail(self, *args, **kw):
        for wizard in self.filtered(lambda w: w.model == "event.guest"):
            active_ids = self.env.context.get("active_ids") or [wizard.res_id]
            self.env[wizard.model].browse(
                active_ids
            ).invited_by = self.env.user.partner_id
        return super().action_send_mail(*args, **kw)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if (
            self.env.context.get("active_model") == "event.guest"
            and self.env.user.partner_id.email
        ):
            res["reply_to"] = self.env.user.partner_id.email
        return res
