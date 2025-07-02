from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class TGWebsiteSale(WebsiteSale):
    def _get_mandatory_fields_billing(self, *args, **kw):
        req = super()._get_mandatory_fields_billing(*args, **kw)
        if not request.env.user._is_public() and "email" in req:
            req.remove("email")
        req.remove("street")
        req.remove("city")
        if "state_id" in req:
            req.remove("state_id")
        if "zip" in req:
            req.remove("zip")
        return req
