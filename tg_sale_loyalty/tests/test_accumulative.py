from odoo import Command
from odoo.tests import new_test_user, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccumulative(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_A = cls.env["product.product"].create(
            {
                "name": "Product A",
                "list_price": 100,
                "sale_ok": True,
                "taxes_id": [(5,)],
            }
        )

        cls.product_B = cls.env["product.product"].create(
            {
                "name": "Product B",
                "list_price": 100,
                "sale_ok": True,
                "taxes_id": [(5,)],
            }
        )

        cls.product_C = cls.env["product.product"].create(
            {
                "name": "Product C",
                "list_price": 100,
                "sale_ok": True,
                "taxes_id": [(5,)],
            }
        )

        cls.user_salemanager = new_test_user(
            cls.env, login="user_salemanager", groups="sales_team.group_sale_manager"
        )

    def _make_programs_and_order(
        self, is_program1_accumulative, is_program2_accumulative
    ):
        LoyaltyProgram = self.env["loyalty.program"]
        LoyaltyProgram.create(
            {
                "name": "Discount code 1 (accumulative)",
                "trigger": "with_code",
                "program_type": "promo_code",
                "applies_on": "current",
                "is_accumulative": is_program1_accumulative,
                "rule_ids": [
                    Command.create(
                        {
                            "mode": "with_code",
                            "code": "test_10pc1",
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

        LoyaltyProgram.create(
            {
                "name": "Discount code 2 (non-accumulative)",
                "trigger": "with_code",
                "program_type": "promo_code",
                "applies_on": "current",
                "is_accumulative": is_program2_accumulative,
                "rule_ids": [
                    Command.create(
                        {
                            "mode": "with_code",
                            "code": "test_10pc2",
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

        order = (
            self.env["sale.order"]
            .with_user(self.user_salemanager)
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

        return order

    def test_accumulative_01(self):
        order = self._make_programs_and_order(True, True)
        self.assertNotIn("error", order._try_apply_code("test_10pc1"))
        self.assertNotIn("error", order._try_apply_code("test_10pc2"))

    def test_accumulative_02(self):
        order = self._make_programs_and_order(True, False)
        self.assertNotIn("error", order._try_apply_code("test_10pc1"))
        self.assertIn("error", order._try_apply_code("test_10pc2"))

    def test_accumulative_03(self):
        order = self._make_programs_and_order(False, True)
        self.assertNotIn("error", order._try_apply_code("test_10pc1"))
        self.assertIn("error", order._try_apply_code("test_10pc2"))

    def test_accumulative_04(self):
        order = self._make_programs_and_order(False, True)
        self.assertNotIn("error", order._try_apply_code("test_10pc1"))
        self.assertIn("error", order._try_apply_code("test_10pc2"))

    def test_promotion_accumulative(self):
        LoyaltyProgram = self.env["loyalty.program"]
        LoyaltyProgram.create(
            {
                "name": "Promotion 1 (accumulative)",
                "trigger": "auto",
                "program_type": "promotion",
                "applies_on": "current",
                "is_accumulative": True,
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "reward_point_mode": "unit",
                            "reward_point_amount": 1,
                            "product_ids": [self.product_A.id],
                        },
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
        LoyaltyProgram.create(
            {
                "name": "Promotion 2 (non-accumulative)",
                "trigger": "auto",
                "program_type": "promotion",
                "applies_on": "current",
                "is_accumulative": True,
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "reward_point_mode": "unit",
                            "reward_point_amount": 1,
                            "product_ids": [self.product_B.id],
                        },
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

        order = (
            self.env["sale.order"]
            .with_user(self.user_salemanager)
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
                        Command.create(
                            {
                                "product_id": self.product_B.id,
                                "tax_id": False,
                            }
                        ),
                    ],
                }
            )
        )

        self.assertEqual(len(order.order_line), 2)

        order._update_programs_and_rewards()
        claimable_rewards = order._get_claimable_rewards()
        for coupon, rewards in claimable_rewards.items():
            res = order._apply_program_reward(rewards, coupon)
            self.assertFalse(bool(res))

        self.assertEqual(len(order.order_line), 4)
