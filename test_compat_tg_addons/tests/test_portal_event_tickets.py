from odoo.tests.common import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserDemo
from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon


@tagged("post_install", "-at_install")
class TestPortalEventTickets(HttpCaseWithUserDemo, TestWebsiteEventSaleCommon):
    def test_upgrade_ticket(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_demo.id,
                "payment_term_id": self.env.ref(
                    "account.account_payment_term_end_following_month"
                ).id,
            }
        )

        sale_order_line = self.env["sale.order.line"].create(
            {
                "product_id": self.env.ref("event_sale.product_product_event").id,
                "price_unit": 190.50,
                "order_id": sale_order.id,
                "event_id": self.event_2.id,
                "event_ticket_id": self.ticket_2.id,
            }
        )

        sale_order.action_confirm()

        reg = self.env["event.registration"].search(
            [
                ("sale_order_id", "=", sale_order.id),
                ("sale_order_line_id", "=", sale_order_line.id),
            ]
        )
        self.assertEqual(reg.partner_id, self.partner_demo)

        event1_reg_count_before = len(self.event.registration_ids)
        event2_reg_count_before = len(self.event_2.registration_ids)

        self.start_tour(
            "/", "tg_website_event_sale_create_event1_registration", 1000, login="demo"
        )
        self.assertEqual(len(self.event.registration_ids), event1_reg_count_before + 1)
        self.assertEqual(len(self.event_2.registration_ids), event2_reg_count_before)

        event1_reg_count_before = len(self.event.registration_ids)
        event2_reg_count_before = len(self.event_2.registration_ids)

        self.start_tour(
            f"/my/tickets/{reg.id}",
            "tg_website_event_sale_change_ticket",
            1000,
            login="demo",
        )

        self.assertEqual(len(self.event.registration_ids), event1_reg_count_before)
        self.assertEqual(
            len(self.event_2.registration_ids), event2_reg_count_before + 1
        )
