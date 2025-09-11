from datetime import datetime

from freezegun import freeze_time

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import tagged

from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon


@tagged("post_install", "-at_install")
class TestPlanGeneration(TestWebsiteEventSaleCommon):
    def test_settings_check_01(self):
        with self.assertRaises(ValidationError):
            self.env["res.config.settings"].create(
                {
                    "invoice_plan_min_deposit_percent": 50,
                    "invoice_plan_max_deposit_percent": 50,
                }
            )

    def test_01(self):
        self.env["res.config.settings"].create(
            {
                "invoice_plan_min_deposit_percent": 50,
                "invoice_plan_max_deposit_percent": 90,
                "invoice_plan_min_deposit_abs": 9999,
            }
        ).execute()

        self.env["sale.order.line"].create(
            {
                "product_id": self.product_event.id,
                "event_id": self.event.id,
                "event_ticket_id": self.ticket.id,
                "order_id": self.so.id,
            }
        )

        with self.assertRaises(UserError) as ctx:
            self.so._generate_invoice_plan_for_event(
                self.ticket.price * 0.8,
                2,
                "month",
            )

        self.assertEqual(
            ctx.exception.args[0],
            "Payment splitting not allowed. Total amount ($ 100.00) is less than minimal absolute deposit amount ($ 9,999.00)",  # noqa: E501
        )

    @freeze_time("2025-09-12")
    def test_02(self):
        self.env["res.config.settings"].create(
            {
                "invoice_plan_min_deposit_percent": 50,
                "invoice_plan_max_deposit_percent": 90,
                "invoice_plan_min_deposit_abs": 0,
                "invoice_plan_security_days": 0,
                "invoice_plan_last_installment_date": False,
            }
        ).execute()

        self.event.write(
            {
                "date_begin": datetime(2026, 2, 27),
                "date_end": datetime(2026, 3, 18),
            }
        )

        so = self.so

        self.env["sale.order.line"].create(
            {
                "product_id": self.product_event.id,
                "event_id": self.event.id,
                "event_ticket_id": self.ticket.id,
                "order_id": so.id,
            }
        )

        with self.assertRaises(UserError) as ctx:
            so._generate_invoice_plan_for_event(
                self.ticket.price * 0.8,
                7,
                "month",
            )

        self.assertEqual(
            ctx.exception.args[0],
            "Last payment date (03/12/2026) exceeds max allowed installment date (02/27/2026)",  # noqa: E501
        )

        p = so._get_split_payment_periods()["month"]
        self.assertEqual(
            so._get_max_installments(p["interval"], p["interval_type"]),
            6,
        )

    @freeze_time("2025-09-12")
    def test_max_installments_01(self):
        self.env["res.config.settings"].create(
            {
                "invoice_plan_min_deposit_percent": 50,
                "invoice_plan_max_deposit_percent": 90,
                "invoice_plan_min_deposit_abs": 0,
                "invoice_plan_security_days": 0,
                "invoice_plan_last_installment_date": datetime(2026, 2, 27),
            }
        ).execute()

        so = self.so
        p = so._get_split_payment_periods()["month"]
        self.assertEqual(
            so._get_max_installments(p["interval"], p["interval_type"]),
            6,
        )
