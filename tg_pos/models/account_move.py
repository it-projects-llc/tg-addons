from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    pos_sessions_origin = fields.Text(
        "Origin (POS Session)",
        help="Origin, that describes, from which POS sessions this invoice is created from",  # noqa: E501
        readonly=True,
    )

    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, *args, **kw):
        if self.env.context.get("no_message_post_body") == kw.get("body", object()):
            return self.env["mail.message"]

        return super().message_post(*args, **kw)
