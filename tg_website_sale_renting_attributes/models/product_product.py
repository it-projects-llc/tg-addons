from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def _get_product_price_context(self, combination):
        res = super()._get_product_price_context(combination)
        if self.rent_via_period_ok:
            period_ptav = combination.filtered("is_period")
            res.update(
                {
                    "start_date": period_ptav.start_date,
                    "end_date": period_ptav.end_date,
                }
            )
        return res
