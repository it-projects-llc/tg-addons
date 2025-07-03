from urllib.parse import quote

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
                base_url = website.domain

                if base_url:
                    for k in res.keys():
                        if isinstance(res[k], str):
                            relative_url = self._get_relative_url(res[k])
                            res[k] = werkzeug.urls.url_join(base_url, relative_url)

        if self.env.context.get("create_user") and self.user_ids.redirect:
            redirect = self.user_ids.redirect
            for k in res.keys():
                if isinstance(res[k], str):
                    res[k] += "&redirect=" + quote(redirect)

        return res

    def _get_relative_url(self, url):
        """Remove scheme and domain from the given URL, returning a relative URL."""
        return werkzeug.urls.url_parse(url).replace(scheme="", netloc="").to_url()
