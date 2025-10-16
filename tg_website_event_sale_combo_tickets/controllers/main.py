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
            if accomodation_category in line.product_id.public_categ_ids:
                accomodation_line = line.product_id.public_categ_ids

        if include_accomodation_flag and not accomodation_line:
            res["hide_payment_button"] = True
            res["should_include_accomodation"] = True

        return res
