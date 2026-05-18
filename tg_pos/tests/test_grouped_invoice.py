from odoo.tests.common import tagged

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@tagged("post_install", "-at_install")
class TestGroupedInvoice(TestPoSCommon):
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
        self.product2 = self.create_product(
            "Product 2",
            self.categ_basic,
            20.0,
            10.0,
            tax_ids=self.taxes["tax10"].ids,
        )
        self.product3 = self.create_product(
            "Product 3",
            self.categ_basic,
            30.0,
            15.0,
            tax_ids=self.taxes["tax_group_7_10"].ids,
        )
        self.product4 = self.create_product(
            "Product 4",
            self.categ_basic,
            54.99,
            tax_ids=[
                self.taxes["tax_fixed006"].id,
                self.taxes["tax_fixed012"].id,
                self.taxes["tax21"].id,
            ],
        )
        self.adjust_inventory(
            [self.product1, self.product2, self.product3], [100, 50, 50]
        )

    def test_merged_invoice_lines(self):
        self.open_new_session()
        self.env["pos.order"].create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product1, 1),
                    ],
                    customer=self.customer,
                )
            ]
        )
        self.env["pos.order"].create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product1, 1),
                    ],
                    customer=self.customer,
                )
            ]
        )
        self.env["pos.order"].create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product2, 1),
                    ],
                    customer=self.customer,
                )
            ]
        )
        self.env["pos.order"].create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product2, 1, 100),
                    ],
                    customer=self.customer,
                )
            ]
        )
        self.env["pos.order"].create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product2, 0),
                    ],
                    customer=self.customer,
                )
            ]
        )
        self.pos_session.action_pos_session_validate()

        action = self.pos_session._generate_grouped_pos_invoice()
        move = self.env["account.move"].browse(action["res_id"])

        product1_invoice_line = move.invoice_line_ids.filtered(
            lambda x: x.product_id == self.product1
        )
        product2_invoice_line = move.invoice_line_ids.filtered(
            lambda x: x.product_id == self.product2
        )

        self.assertEqual(len(product1_invoice_line), 1)
        self.assertEqual(len(product2_invoice_line), 1)

    def test_refund(self):
        self.open_new_session()
        PosOrder = self.env["pos.order"]
        PosOrder.create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product1, 1),
                    ],
                    customer=self.customer,
                )
            ]
        )
        order_datas = PosOrder.create_from_ui(
            [
                self.create_ui_order_data(
                    [
                        (self.product1, 1),
                    ],
                    customer=self.customer,
                )
            ]
        )

        # make refund order and pay
        pos_order_to_refund = PosOrder.browse(order_datas[0]["id"])
        refund_order = pos_order_to_refund._refund()

        make_payment = (
            self.env["pos.make.payment"]
            .with_context(
                active_ids=[refund_order.id],
                active_id=refund_order.id,
            )
            .create(
                {
                    "payment_method_id": self.cash_pm1.id,
                    "amount": -pos_order_to_refund.amount_total,
                }
            )
        )
        make_payment.check()

        self.pos_session.action_pos_session_validate()

        action = self.pos_session._generate_grouped_pos_invoice()
        move = self.env["account.move"].browse(action["res_id"])

        product1_invoice_lines = move.invoice_line_ids.filtered(
            lambda x: x.product_id == self.product1
        )

        self.assertEqual(len(product1_invoice_lines), 1)
        self.assertEqual(product1_invoice_lines[0].quantity, 1)
