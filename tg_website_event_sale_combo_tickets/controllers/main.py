from odoo.addons.website_sale.controllers.main import WebsiteSale


class TGWebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        res = super()._get_shop_payment_values(order, **kwargs)

        include_accomodation_flag = False
        accomodation_line = False
        accomodation_category = order.company_id.accomodation_category
        if not accomodation_category:
            return res

        for line in order.order_line:
            include_accomodation_flag = (
                line.event_ticket_id.include_accomodation or include_accomodation_flag
            )
            if (
                accomodation_category
                in line.product_id.public_categ_ids.parents_and_self
            ):
                accomodation_line = line

        if include_accomodation_flag and not accomodation_line:
            res.update(
                {
                    "hide_payment_button": True,
                    "should_include_accomodation": True,
                    "accomodation_category_url": f"/shop/category/{accomodation_category.id}",  # noqa: E501
                    "errors": [None],
                }
            )

        return res
