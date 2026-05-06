from odoo.http import request
from odoo.tools.misc import str2bool

from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class TGWebsiteAuthSignupHome(AuthSignupHome):
    def get_auth_signup_qcontext(self):
        qcontext = super().get_auth_signup_qcontext()
        if "tnc_accepted" in request.params:
            qcontext["tnc_accepted"] = str2bool(request.params["tnc_accepted"])
        return qcontext

    def _prepare_signup_values(self, qcontext, *args, **kw):
        values = super()._prepare_signup_values(qcontext, *args, **kw)
        if "tnc_accepted" in qcontext:
            values["tnc_accepted"] = qcontext["tnc_accepted"]
        return values
