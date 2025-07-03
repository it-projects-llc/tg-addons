from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestPosGroupButtonsTour(HttpCase):
    def test_customer_button(self):
        group = self.env.ref("tg_pos.group_show_customer_button")
        admin_user = self.env.ref("base.user_admin")
        demo_user = self.env.ref("base.user_demo")

        admin_user.write({"groups_id": [(4, group.id)]})
        self.start_tour("/pos/ui", "tg_pos.customer_button_visible", login="admin")

        demo_user.write({"groups_id": [(3, group.id)]})
        self.start_tour("/pos/ui", "tg_pos.customer_button_hidden", login="demo")
