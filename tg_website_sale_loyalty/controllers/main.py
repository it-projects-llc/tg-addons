from odoo.http import request, route

from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController


class TGWebsiteEventSaleController(WebsiteEventSaleController):
    @route()
    def registration_confirm(self, event, **post):
        res = super().registration_confirm(event, **post)
        order_sudo = request.website.sale_get_order()
        customer_nationality = order_sudo.partner_id.nationality_id
        if customer_nationality:
            ndp = request.env["nationality.discount.program"].search(
                [
                    ("nationality", "=", customer_nationality.id),
                    ("company_id", "in", (request.env.company.id, False)),
                ],
                limit=1,
            )
            if ndp.discount_code:
                order_sudo._try_apply_code(ndp.discount_code)
        return res
