from odoo.addons.website_sale_renting.controllers.main import (
    WebsiteSaleRenting,
    request,
)


class TGWebsiteSaleRenting(WebsiteSaleRenting):
    def _prepare_product_values(self, product, *args, **kwargs):
        res = super()._prepare_product_values(product, *args, **kwargs)
        order_sudo = request.website.sale_get_order()
        res["deny_rent_this_product"] = not order_sudo._can_rent_this_product(product)
        return res

    def _cart_values(self, **post):
        res = super()._cart_values(**post)
        order = request.website.sale_get_order()
        if order and res["suggested_products"]:
            res["suggested_products"] = list(
                filter(
                    lambda x: not x.rent_ok or order._can_rent_this_product(x),
                    res["suggested_products"],
                )
            )
        return res
