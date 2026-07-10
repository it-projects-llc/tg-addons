from odoo.tests.common import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon


@tagged("post_install", "-at_install")
class TestUi(HttpCaseWithUserDemo, TestWebsiteEventSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner_panama = cls.env["res.partner"].create(
            {
                "name": "Noa Noa",
                "email": "noa@example.com",
                "nationality_id": cls.env.ref("base.pa").id,
                "country_id": cls.env.ref("base.pa").id,
                "street": "Streeet",
                "city": "Panama",
                "zip": "0801",
            }
        )

        cls.user_panama = cls.env["res.users"].create(
            {
                "login": "panama",
                "password": "panama",
                "partner_id": cls.partner_panama.id,
                "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
            }
        )

        cls.partner_demo.nationality_id = cls.env.ref("base.us")

        cls.p1 = cls.env["loyalty.program"].create(
            {
                "name": "Code for 10% on orders",
                "trigger": "with_code",
                "program_type": "promo_code",
                "applies_on": "current",
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "mode": "with_code",
                            "code": "test_10pc",
                        },
                    )
                ],
                "reward_ids": [
                    (
                        0,
                        0,
                        {
                            "reward_type": "discount",
                            "discount_mode": "percent",
                            "discount": 10,
                            "discount_applicability": "order",
                            "required_points": 1,
                        },
                    )
                ],
            }
        )

        cls.ndp = cls.env["nationality.discount.program"].create(
            {
                "nationality": cls.env.ref("base.pa").id,
                "discount_program": cls.p1.id,
            }
        )

    def test_buy_panama(self):
        if self.env["ir.module.module"]._get("payment_custom").state != "installed":
            self.skipTest("Transfer provider is not installed")

        transfer_provider = self.env.ref("payment.payment_provider_transfer")
        transfer_provider.write(
            {
                "state": "enabled",
                "is_published": True,
            }
        )
        transfer_provider._transfer_ensure_pending_msg_is_set()

        #  Ensure the use of USD (company currency)
        self.env["product.pricelist"].create({"name": "Public Pricelist"})

        self.start_tour(
            "/", "panama_event_buy_tickets", login="panama", step_delay=1000
        )

    def test_buy_not_panama(self):
        if self.env["ir.module.module"]._get("payment_custom").state != "installed":
            self.skipTest("Transfer provider is not installed")

        transfer_provider = self.env.ref("payment.payment_provider_transfer")
        transfer_provider.write(
            {
                "state": "enabled",
                "is_published": True,
            }
        )
        transfer_provider._transfer_ensure_pending_msg_is_set()

        #  Ensure the use of USD (company currency)
        self.env["product.pricelist"].create({"name": "Public Pricelist"})

        self.start_tour(
            "/",
            f"not_panama_event_buy_tickets_and_try_apply_{self.ndp.discount_code}",
            login="demo",
            step_delay=1000,
        )
