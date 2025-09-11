from datetime import timedelta

from odoo.tests.common import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon


@tagged("post_install", "-at_install")
class TestFrontend(HttpCaseWithUserDemo, TestWebsiteEventSaleCommon):
    def setUp(self):
        super().setUp()

        if self.env["ir.module.module"]._get("payment_custom").state != "installed":
            self.skipTest("Transfer provider is not installed")

        self.env.ref("payment.payment_provider_transfer").write(
            {
                "state": "enabled",
                "is_published": True,
            }
        )

    def test_split_payment_01(self):
        self.event.write(
            {
                "date_begin": self.event.date_begin + timedelta(days=30),
                "date_end": self.event.date_end + timedelta(days=30),
            }
        )

        self.env["res.config.settings"].create(
            {
                "invoice_plan_min_deposit_abs": 100,
                "invoice_plan_last_installment_date": self.event.date_begin,
                "invoice_plan_security_days": 0,
            }
        ).execute()

        self.start_tour(
            "/event", "tg_website_event_sale_split_payments_tour_1", 1000, login="demo"
        )
