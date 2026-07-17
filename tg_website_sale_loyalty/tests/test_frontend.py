from odoo.tests.common import tagged

from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon

from .common import TGSaleLoyaltyCommon


@tagged("post_install", "-at_install")
class TestUi(TestWebsiteEventSaleCommon, TGSaleLoyaltyCommon):
    def test_buy_panama_event(self):
        self.start_tour(
            "/", "panama_event_buy_tickets", login="panama", step_delay=1000
        )

    def test_buy_not_panama_event(self):
        self.start_tour(
            "/",
            f"not_panama_event_buy_tickets_and_try_apply_{self.ndp.discount_code}",
            login="demo",
            step_delay=1000,
        )

    def test_buy_panama_not_event(self):
        self.start_tour("/", "panama_not_event_buy", login="panama", step_delay=1000)

    def test_buy_not_panama_not_event(self):
        self.start_tour(
            "/",
            f"not_panama_not_event_buy_and_try_apply_{self.ndp.discount_code}",
            login="demo",
            step_delay=1000,
        )
