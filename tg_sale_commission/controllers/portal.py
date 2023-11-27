from odoo.exceptions import AccessError, MissingError
from odoo.http import request, route

from odoo.addons.tg_website_sale_affiliate.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    @route(
        "/my/affiliates/<int:affiliate_id>/orders",
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_affiliate_orders(self, affiliate_id, **kw):
        try:
            # TODO: add security rules
            affiliate = self._document_check_access("sale.affiliate", affiliate_id)
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._prepare_portal_layout_values()

        SaleOrder = request.env["sale.order"]
        order_ids = affiliate._get_order_dict().get(affiliate.id, [])
        domain = [("id", "in", order_ids)]

        orders = SaleOrder.sudo().search(domain)
        values.update(
            {
                "orders": orders,
                "affiliate": affiliate,
                "page_name": "affiliate",
            }
        )

        return request.render("tg_sale_commission.portal_my_orders", values)
