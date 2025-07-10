from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@tagged("post_install", "-at_install")
class TestPosCustomerButtonVisible(TestPointOfSaleHttpCommon):
    def test_customer_button_visible(self):
        """Check that customer button is visible for user in group"""
        group = self.env.ref("tg_pos.group_show_customer_button")

        self.pos_user.write({"groups_id": [(4, group.id)]})

        self.start_tour(
            f"/pos/ui?config_id={self.main_pos_config.id}",
            "tg_pos.customer_button_visible",
            login=self.pos_user.login,
        )
