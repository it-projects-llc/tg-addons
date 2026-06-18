from odoo.addons.website_sale_renting.controllers.main import (
    WebsiteSaleRenting,
    request,
    route,
)


class TGWebsiteSaleRenting(WebsiteSaleRenting):
    def _prepare_product_values(self, product, *args, **kwargs):
        res = super()._prepare_product_values(product, *args, **kwargs)
        order_sudo = request.website.sale_get_order()
        res["deny_rent_this_product"] = not order_sudo._can_rent_this_product(product)
        return res

    @route()
    def cart(self, *args, **kw):
        res = super().cart(*args, **kw)
        order = res.qcontext.get("website_sale_order")
        if order and res.qcontext.get("suggested_products"):
            res.qcontext["suggested_products"] = list(
                filter(
                    lambda x: not x.rent_ok or order._can_rent_this_product(x),
                    res.qcontext["suggested_products"],
                )
            )
        return res
