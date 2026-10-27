from datetime import date, datetime

from odoo.addons.sale.tests.common import SaleCommon


class TestMain(SaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pa = cls.env["product.attribute"].create(
            {
                "name": "Period",
                "create_variant": "no_variant",
                "is_period": True,
                "value_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "1-10",
                            "default_start_date": date(2026, 9, 1),
                            "default_end_date": date(2026, 9, 10),
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "11-20",
                            "default_start_date": date(2026, 9, 11),
                            "default_end_date": date(2026, 9, 20),
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "21-30",
                            "default_start_date": date(2026, 9, 21),
                            "default_end_date": date(2026, 9, 30),
                        },
                    ),
                ],
            }
        )

        cls.pt = cls.env["product.template"].create(
            {
                "name": "Example Period Product",
                "rent_via_period_ok": True,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.pa.id,
                            "value_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        cls.pa.value_ids[0].id,
                                        cls.pa.value_ids[1].id,
                                        cls.pa.value_ids[2].id,
                                    ],
                                )
                            ],
                        },
                    )
                ],
                "list_price": 100,
                "taxes_id": [(5,)],
            }
        )

        cls.pp = cls.pt.product_variant_id

        cls.ptav1 = cls.pt.attribute_line_ids[0].product_template_value_ids[0]
        cls.ptav2 = cls.pt.attribute_line_ids[0].product_template_value_ids[1]
        cls.ptav3 = cls.pt.attribute_line_ids[0].product_template_value_ids[2]

        cls.ptav1.write(
            {
                "price_extra": 10,
            }
        )
        cls.ptav2.write(
            {
                "price_extra": 20,
            }
        )
        cls.ptav3.write(
            {
                "price_extra": 30,
            }
        )

    def test_sale_order_rent_01(self):
        so = (
            self.env["sale.order"]
            .with_context(in_rental_app=True)
            .create(
                {
                    "partner_id": self.partner.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": self.pp.id,
                                "product_no_variant_attribute_value_ids": [
                                    (6, 0, [self.ptav1.id])
                                ],
                            },
                        )
                    ],
                }
            )
        )
        self.assertEqual(so.rental_start_date, datetime(2026, 9, 1, 5, 0))
        self.assertEqual(so.rental_return_date, datetime(2026, 9, 10, 5, 0))
        self.assertEqual(so.amount_total, 110)

        so.action_confirm()
        self.assertTrue(
            self.env["sale.rental.schedule"].search([("order_id", "=", so.id)])
        )

    def test_sale_order_rent_02(self):
        so = (
            self.env["sale.order"]
            .with_context(in_rental_app=True)
            .create(
                {
                    "partner_id": self.partner.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": self.pp.id,
                                "product_no_variant_attribute_value_ids": [
                                    (6, 0, [self.ptav2.id])
                                ],
                            },
                        )
                    ],
                }
            )
        )
        self.assertEqual(so.rental_start_date, datetime(2026, 9, 11, 5, 0))
        self.assertEqual(so.rental_return_date, datetime(2026, 9, 20, 5, 0))
        self.assertEqual(so.amount_total, 120)

        so.action_confirm()
        self.assertTrue(
            self.env["sale.rental.schedule"].search([("order_id", "=", so.id)])
        )

    def test_sale_order_rent_03(self):
        so = (
            self.env["sale.order"]
            .with_context(in_rental_app=True)
            .create(
                {
                    "partner_id": self.partner.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": self.pp.id,
                                "product_no_variant_attribute_value_ids": [
                                    (6, 0, [self.ptav3.id])
                                ],
                            },
                        )
                    ],
                }
            )
        )
        self.assertEqual(so.rental_start_date, datetime(2026, 9, 21, 5, 0))
        self.assertEqual(so.rental_return_date, datetime(2026, 9, 30, 5, 0))
        self.assertEqual(so.amount_total, 130)

        so.action_confirm()
        self.assertTrue(
            self.env["sale.rental.schedule"].search([("order_id", "=", so.id)])
        )
