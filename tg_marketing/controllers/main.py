from odoo.http import request, route

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventMarketing(WebsiteEventController):
    @route()
    def registration_confirm(self, event, **post):
        res = super().registration_confirm(event, **post)

        MarketingAnswers = request.env["res.partner.marketing.answer"].sudo()
        partner_marketing_vals = {}
        for key, value in post.items():
            if "marketing_answer" in key and value:
                dummy, registration_index, field_name = key.split("-")
                try:
                    value_answer_id = int(value)
                    value_answer = MarketingAnswers.browse(value_answer_id).exists()
                    if not value_answer:
                        raise ValueError()
                    if value_answer.field.name != field_name:
                        raise ValueError()

                    partner_marketing_vals[field_name] = value_answer_id

                except (IndexError, ValueError):
                    value_answer = MarketingAnswers._create_custom_answer(
                        field_name, value
                    )
                    partner_marketing_vals[field_name] = value_answer.id

        if partner_marketing_vals:
            request.env.user.partner_id.sudo().write(partner_marketing_vals)

        return res
