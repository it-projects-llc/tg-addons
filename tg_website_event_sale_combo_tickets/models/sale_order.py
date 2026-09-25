from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _should_include_accomodation(self):
        self.ensure_one()

        has_positive_accomodation_answers = False
        accomodation_line = False
        accomodation_category = self.company_id.accomodation_category
        if not accomodation_category:
            return False

        for line in self.order_line:
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
            return True
        else:
            return False
