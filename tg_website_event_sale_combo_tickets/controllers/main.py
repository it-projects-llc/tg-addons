from odoo.addons.website_sale.controllers.main import WebsiteSale


class TGWebsiteSale(WebsiteSale):
    def _get_shop_payment_values(self, order, **kwargs):
        res = super()._get_shop_payment_values(order, **kwargs)

        has_positive_accomodation_answers = False
        accomodation_line = False
        accomodation_category = order.company_id.accomodation_category
        if not accomodation_category:
            return res

        for line in order.order_line:
            has_positive_accomodation_answers = (
                has_positive_accomodation_answers
                or any(
                    line.registration_ids.registration_answer_choice_ids.filtered(
                        lambda x: x.question_id.is_accomodation
                    ).mapped("value_answer_id.is_positive_accomodation_answer")
                )
            )

            if (
                accomodation_category
                in line.product_id.public_categ_ids.parents_and_self
            ):
                accomodation_line = line

        if has_positive_accomodation_answers and not accomodation_line:
            res.update(
                {
                    "hide_payment_button": True,
                    "should_include_accomodation": True,
                    "accomodation_category_url": f"/shop/category/{accomodation_category.id}",  # noqa: E501
                    "errors": [None],
                }
            )

        return res
