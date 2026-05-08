from psycopg2.errors import ForeignKeyViolation

from odoo.tests.common import tagged
from odoo.tools.misc import mute_logger

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@tagged("post_install", "-at_install")
class TestMisc(TestPoSCommon):
    def setUp(self):
        super().setUp()

        self.config = self.basic_config
        self.product1 = self.create_product(
            "Product 1",
            self.categ_basic,
            10.0,
            5.0,
            tax_ids=self.taxes["tax7"].ids,
        )

        self.adjust_inventory([self.product1], [100])

    @mute_logger("odoo.sql_db")
    def test_delete_customer_restrict(self):
        customer = self.env["res.partner"].create(
            {
                "name": "Customer ttt",
                "property_account_receivable_id": self.c1_receivable.id,
            }
        )
        self.open_new_session()
        self.env["pos.order"].create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product1, 1),
                    ],
                    customer=customer,
                )
            ]
        )

        with self.assertRaises(ForeignKeyViolation):
            customer.unlink()
