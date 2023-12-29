from odoo import models


class SaleCouponApplyCode(models.TransientModel):
    _inherit = "sale.coupon.apply.code"

    def apply_coupon(self, order, coupon_code):
        if coupon_code:
            SaleAffiliate = self.sudo().env["sale.affiliate"]
            affiliate = SaleAffiliate.search(
                [("promo_code", "=", coupon_code)], limit=1
            )

            if affiliate:
                order.affiliate_request_id = affiliate.get_request()
                order.recompute_coupon_lines()
                return {
                    "generated_coupon": {
                        "code": coupon_code,
                        "reward": affiliate.code_promo_program_id.discount_line_product_id.name,
                    },
                }
        return super(SaleCouponApplyCode, self).apply_coupon(order, coupon_code)
