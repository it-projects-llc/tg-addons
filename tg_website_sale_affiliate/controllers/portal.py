from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    def _prepare_affiliates_domain(self, partner):
        return [("partner_id", "in", partner.ids)]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        Affiliate = request.env["sale.affiliate"]
        if "affiliate_count" in counters:
            values["affiliate_count"] = (
                Affiliate.search_count(self._prepare_affiliates_domain(partner))
                if Affiliate.check_access_rights("read", raise_exception=False)
                else 0
            )

        return values

    @route("/my/affiliates", type="http", auth="user", website=True)
    def portal_my_affiliates(self, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        Affiliate = request.env["sale.affiliate"]
        domain = self._prepare_affiliates_domain(partner)

        affiliates = Affiliate.search(domain)

        values.update(
            {
                "affiliates": affiliates,
                "page_name": "affiliate",
            }
        )

        return request.render("tg_website_sale_affiliate.portal_my_affiliates", values)
