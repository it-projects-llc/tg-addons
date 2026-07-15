from odoo.tests.common import tagged

from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon


@tagged("post_install", "-at_install")
class TestMisc(TestWebsiteEventSaleCommon):
    def test_not_sellable_line(self):
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
            "/", "tg_website_event_sale_create_event2_registration", 1000, login="demo"
        )
        self.assertEqual(len(self.event.registration_ids), event1_reg_count_before - 1)
        self.assertEqual(
            len(self.event_2.registration_ids), event2_reg_count_before + 1
        )
