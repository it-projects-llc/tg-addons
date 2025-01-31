from odoo import Command
from odoo.tests import new_test_user, tagged

from odoo.addons.sale_loyalty.tests.common import TestSaleCouponCommon


@tagged("post_install", "-at_install")
class TestLoyalty(TestSaleCouponCommon):
    def test_coupon_with_spaces(self):
        user_salemanager = new_test_user(
            self.env, login="user_salemanager", groups="sales_team.group_sale_manager"
        )

        LoyaltyProgram = self.env["loyalty.program"]
        LoyaltyProgram.create(
            {
                "name": "Code for 10% on orders",
                "trigger": "with_code",
                "program_type": "promotion",
                "applies_on": "current",
                "rule_ids": [
                    Command.create(
                        {
                            "mode": "with_code",
                            "code": "test_10pc",
                        }
                    )
                ],
                "reward_ids": [
                    Command.create(
                        {
                            "reward_type": "discount",
                            "discount_mode": "percent",
                            "discount": 10,
                            "discount_applicability": "order",
                            "required_points": 1,
                        }
                    )
                ],
            }
        )

        # based on test_points_awarded_global_discount_code_no_domain_program
        loyalty_program = LoyaltyProgram.create(
            LoyaltyProgram._get_template_values()["loyalty"]
        )
        loyalty_card = self.env["loyalty.card"].create(
            {
                "program_id": loyalty_program.id,
                "partner_id": self.partner_a.id,
                "points": 0,
            }
        )

        order = (
            self.env["sale.order"]
            .with_user(user_salemanager)
            .create(
                {
                    "partner_id": self.partner_a.id,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": self.product_A.id,
                                "tax_id": False,
                            }
                        ),
                    ],
                }
            )
        )

        self.assertEqual(order.amount_total, 100)
        self._apply_promo_code(order, " test_10pc ")  # changed here: spaces added
        self.assertEqual(order.amount_total, 90)
        order.action_confirm()
        self.assertEqual(loyalty_card.points, 90)
