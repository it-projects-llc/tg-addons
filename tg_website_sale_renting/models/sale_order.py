from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_products_with_specific_renting_period(self):
        res = self.env["product.template"]

        products = self.mapped("order_line.product_template_id")
        for product in products:
            if not product.rent_ok:
                continue

            if product.renting_min_start_date or product.renting_max_end_date:
                res |= product

        return res

    def _get_allowed_renting_periods(self):
        if not self.order_line:
            return []

        self.ensure_one()
        p = self._get_products_with_specific_renting_period()
        return list(set(p._get_allowed_renting_periods(self.company_id)))

    def _can_rent_this_product(self, product):
        if not self:
            return True

        if product._name == "product.product":
            product = product.product_tmpl_id

        self.ensure_one()
        all_products = self.mapped("order_line.product_template_id")
        if not all_products:
            return True

        product_renting_period = (
            product.renting_min_start_date,
            product.renting_max_end_date,
        )
        is_adding_product_with_specific_renting_period = bool(
            product.renting_min_start_date or product.renting_max_end_date
        )
        existing_products_with_specific_renting_period = (
            self._get_products_with_specific_renting_period()
        )
        other_products = all_products - existing_products_with_specific_renting_period

        if (
            is_adding_product_with_specific_renting_period
            and existing_products_with_specific_renting_period
            and (
                product in existing_products_with_specific_renting_period
                or (product_renting_period in self._get_allowed_renting_periods())
            )
        ):
            return True
        elif not is_adding_product_with_specific_renting_period and other_products:
            return True
        else:
            return False
