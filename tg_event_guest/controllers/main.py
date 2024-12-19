from odoo import _
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import (
    AuthSignupHome as BaseAuthSignupHome,
)


class AuthSignupHome(BaseAuthSignupHome):
    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()
        if not qcontext.get("guest_register_code") and request.params.get(
            "guest_register_code"
        ):
            qcontext["guest_register_code"] = request.params.get("guest_register_code")

        guest_register_code = qcontext.get("guest_register_code")
        if guest_register_code:
            guest = request.env["event.guest"]._get_by_code(guest_register_code)
            if guest:
                if not qcontext.get("name"):
                    qcontext["name"] = guest.name or ""
                if not qcontext.get("login"):
                    qcontext["login"] = guest.email or ""
                if request.session.uid:
                    qcontext["error"] = _("You need to logout to register guest")

        return qcontext

    def _prepare_signup_values(self, qcontext):
        values = super()._prepare_signup_values(qcontext)
        if qcontext.get("guest_register_code"):
            values["guest_register_code"] = qcontext["guest_register_code"]
        return values
