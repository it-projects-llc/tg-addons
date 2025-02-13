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

    def _make_programs_and_order(
        self, is_program1_accumulative, is_program2_accumulative
    ):
        user_salemanager = new_test_user(
            self.env, login="user_salemanager", groups="sales_team.group_sale_manager"
        )

        LoyaltyProgram = self.env["loyalty.program"]
        LoyaltyProgram.create(
            {
                "name": "Promo 1 (accumulative)",
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
                "name": "Promo 2 (non-accumulative)",
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

        return order

    def _test_accumulative_01(self):
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
