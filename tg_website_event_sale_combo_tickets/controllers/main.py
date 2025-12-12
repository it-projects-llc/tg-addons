from odoo.http import request

from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteEventSaleComboTicketsController(WebsiteEventSaleController):
    def _process_attendees_form(self, event, form_details):
        registrations = super()._process_attendees_form(event, form_details)
        extra_registrations = []
        for reg in registrations:
            answers = reg.get("registration_answer_ids") or []
            for answer in answers:
                answer_id = answer[2].get("value_answer_id")
                answer_record = request.env["event.question.answer"].browse(answer_id)
                if answer_record.question_id.is_shuttle:
                    extra_reg = reg.copy()
                    extra_reg.update(event_ticket_id=answer_record.shuttle_ticket.id)
                    extra_registrations.append(extra_reg)
        return registrations + extra_registrations


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
