from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@tagged("post_install", "-at_install")
class TestPosUi(TestPointOfSaleHttpCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer_button_group = cls.env.ref("tg_pos.group_show_customer_button")

    def test_customer_button_visible(self):
        """Customer button is visible when user in group"""
        self.pos_user.write({"groups_id": [(4, self.customer_button_group.id)]})

        self.start_tour(
            f"/pos/ui?config_id={self.main_pos_config.id}",
            "tg_pos.customer_button_visible",
            login=self.pos_user.login,
        )

    def test_customer_button_hidden(self):
        """Customer button is hidden when user not in group"""
        self.pos_user.write({"groups_id": [(3, self.customer_button_group.id)]})

        self.start_tour(
            f"/pos/ui?config_id={self.main_pos_config.id}",
            "tg_pos.customer_button_hidden",
            login=self.pos_user.login,
        )
