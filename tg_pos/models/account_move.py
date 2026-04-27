from odoo import api, fields, models

sentinel = object()


class AccountMove(models.Model):
    _inherit = "account.move"

    pos_sessions_origin = fields.Text(
        "Origin (POS Sessions)",
        help="The origin that describes which POS session(s) this invoice is created from",  # noqa: E501
        readonly=True,
    )

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, *args, **kw):
        if self.env.context.get("no_message_post") == sentinel:
            return self.env["mail.message"]

        return super().message_post(*args, **kw)
