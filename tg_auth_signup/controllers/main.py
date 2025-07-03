from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class TGAuthSignupHome(AuthSignupHome):
    def _prepare_signup_values(self, qcontext):
        values = super()._prepare_signup_values(qcontext)
        if "redirect" in qcontext and not qcontext.get("password"):
            values["redirect"] = qcontext["redirect"]
        return values
