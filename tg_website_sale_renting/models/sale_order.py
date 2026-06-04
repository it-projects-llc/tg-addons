from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _has_product_specific_renting_period(self):
        products = self.mapped("order_line.product_template_id")
        for product in products:
            if not product.rent_ok:
                continue

            if product.renting_min_start_date or product.renting_max_date:
                return True

        return False
