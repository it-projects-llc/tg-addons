from odoo import _, models
from odoo.exceptions import ValidationError


class SaleCouponApplyCode(models.TransientModel):
    _inherit = "sale.loyalty.coupon.wizard"

    def action_apply(self):
        self.ensure_one()
        if not self.order_id:
            raise ValidationError(_("Invalid sales order."))

        status = self.order_id._try_apply_code(self.coupon_code)
        if "error" in status:
            raise ValidationError(status["error"])

        all_rewards = self.env["loyalty.reward"]
        for rewards in status.values():
            all_rewards |= rewards

        if self.coupon_code:
            SaleAffiliate = self.sudo().env["sale.affiliate"]
            affiliate = SaleAffiliate.search(
                [("promo_code", "=", self.coupon_code)], limit=1
            )
            if affiliate:
                self.order_id.affiliate_request_id = affiliate.get_request()
                self.order_id.recompute_coupon_lines()
                reward = affiliate.code_promo_program_id.discount_line_product_id.name
                return {
                    "generated_coupon": {
                        "code": self.coupon_code,
                        "reward": reward,
                    },
                }

        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_loyalty.sale_loyalty_reward_wizard_action"
        )
        action["context"] = {
            "active_id": self.order_id.id,
            "default_reward_ids": all_rewards.ids,
        }

        return action
