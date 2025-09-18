from odoo import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccount(AccountTestInvoicingCommon):
    def test_precision_fixes(self):
        self.env["res.config.settings"].create(
            {
                "invoice_plan_min_deposit_percent": 0,
                "invoice_plan_max_deposit_percent": 100,
                "invoice_plan_min_deposit_abs": 10,
            }
        ).execute()

        product_a_income_account = self.product_a._get_product_accounts()["income"]
        product_b_income_account = self.product_b._get_product_accounts()["income"]
        self.assertNotEqual(
            product_a_income_account,
            product_b_income_account,
            "Test products should have different income accounts for this test",
        )
        so = (
            self.env["sale.order"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "partner_id": self.partner_a.id,
                    "order_line": [
                        Command.create(
                            {
                                "name": self.product_a.name,
                                "product_id": self.product_a.id,
                                "product_uom_qty": 1,
                                "product_uom": self.product_a.uom_id.id,
                                "price_unit": self.product_a.list_price,
                                "tax_id": False,
                            }
                        ),
                        Command.create(
                            {
                                "name": self.product_b.name,
                                "product_id": self.product_b.id,
                                "product_uom_qty": 1,
                                "product_uom": self.product_b.uom_id.id,
                                "price_unit": self.product_b.list_price,
                                "tax_id": False,
                            }
                        ),
                    ],
                }
            )
        )

        account_sums_from_so = so._calculate_income_accounts()
        self.assertEqual(account_sums_from_so[product_a_income_account], 1000)
        self.assertEqual(account_sums_from_so[product_b_income_account], 200)

        so._generate_invoice_plan_for_event(
            100,
            5,
            "month",
        )
        so._prepare_first_plan_payment()

        account_sums_from_invoices = so.order_line.mapped(
            "invoice_lines.move_id"
        )._calculate_accounts()

        self.assertEqual(
            account_sums_from_so[product_a_income_account],
            account_sums_from_invoices[product_a_income_account],
        )
        self.assertEqual(
            account_sums_from_so[product_b_income_account],
            account_sums_from_invoices[product_b_income_account],
        )
