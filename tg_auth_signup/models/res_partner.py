import werkzeug.urls

from odoo import api, models


class Partner(models.Model):
    _inherit = "res.partner"

    @api.depends_context("website_id")
    def _compute_signup_url(self):
        return super()._compute_signup_url()

    def _get_signup_url_for_action(self, *args, **kw):
        res = super()._get_signup_url_for_action(*args, **kw)
        if not self.env.context.get("relative_url"):
            website = self.env["website"].get_current_website()
            if website:
                base_url = website._get_http_domain()

                if base_url:
                    for k in res.keys():
                        relative_url = website._get_relative_url(res[k])
                        res[k] = werkzeug.urls.url_join(base_url, relative_url)

        return res
