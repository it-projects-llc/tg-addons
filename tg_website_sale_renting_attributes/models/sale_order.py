from odoo import _, api, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _enforce_rental_dates(self):
        for record in self.with_context(enforcing_rental_dates=True):
            expected_start_date = False
            expected_end_date = False
            line_with_expected = self.env["sale.order.line"]

            for line in record.order_line.filtered(lambda x: not x.display_type):
                if not line.product_id.rent_via_period_ok:
                    continue

                start_date, end_date = line._detect_start_end_date()

                if expected_start_date and expected_start_date != start_date:
                    raise UserError(
                        _(
                            "Conflict in start dates: %(expected_start_date)s from %(description_from_expected)s conflicts with %(given_start_date)s from %(description_from_given)s",  # noqa: E501
                            expected_start_date=expected_start_date,
                            description_from_expected=line_with_expected.display_name,
                            given_start_date=start_date,
                            description_from_given=line.display_name,
                        )
                    )

                if expected_end_date and expected_end_date != end_date:
                    raise UserError(
                        _(
                            "Conflict in end dates: %(expected_end_date)s from %(description_from_expected)s conflicts with %(given_end_date)s from %(description_from_given)s",  # noqa: E501
                            expected_end_date=expected_end_date,
                            description_from_expected=line_with_expected.display_name,
                            given_end_date=end_date,
                            description_from_given=line.display_name,
                        )
                    )

                expected_start_date = start_date
                expected_end_date = end_date
                line_with_expected = line

            if line_with_expected:
                record.rental_start_date = expected_start_date
                record.rental_return_date = expected_end_date

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._enforce_rental_dates()
        return records

    def write(self, vals):
        should_enforce = not self.env.context.get("enforcing_rental_dates") and (
            "order_line" in vals
        )
        res = super().write(vals)
        if should_enforce:
            self._enforce_rental_dates()
        return res

    def _show_renting_dates_on_cart(self):
        res = super()._show_renting_dates_on_cart()
        if not res:
            return res

        return not any(self.mapped("order_line.product_id.rent_via_period_ok"))

    def _can_rent_this_product(self, product):
        if product.rent_via_period_ok and any(
            self.mapped("order_line.product_id.rent_ok")
        ):
            return False

        return super()._can_rent_this_product(product)
