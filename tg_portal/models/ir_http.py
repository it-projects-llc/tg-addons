from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _get_signin_url(cls):
        base_url = "/web/login"

        for path in (
            request.httprequest.path,
            request.httprequest.values.get("redirect") or "",
        ):
            if not path.endswith("/login"):
                return f"{base_url}?redirect={path}"

        return base_url
