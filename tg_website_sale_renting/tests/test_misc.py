from datetime import datetime

from freezegun import freeze_time

from odoo.tests import HttpCase

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_sale_renting.tests.common import TestWebsiteSaleRentingCommon


class TestMisc(HttpCase, TestWebsiteSaleRentingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chainsaw = cls.env["product.product"].create(
            {
                "name": "Chainsawr",
                "list_price": 2000,
                "rent_ok": True,
            }
        )

    @freeze_time("2026, 1, 1")
    def test_igor_report_task4332_2026_05_22(self):
        self.company.write(
            {
                "renting_default_start_date": "2026-05-26",
                "renting_default_end_date": "2026-05-29",
            }
        )
        self.computer.write(
            {
                "company_id": self.company.id,
            }
        )
        with MockRequest(self.env, cookies={"tz": "Asia/Yekaterinburg"}):
            self.computer.product_tmpl_id._get_default_renting_dates(
                False, False, 1, "day"
            )

    def make_so(self):
        so = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "rental_start_date": datetime(2026, 5, 27),
                "rental_return_date": datetime(2026, 5, 28),
            }
        )

        self.env["sale.order.line"].create(
            {
                "order_id": so.id,
                "product_id": self.computer.id,
            }
        )

        return so

    @freeze_time("2026, 1, 1")
    def test_allowed_to_rent_01(self):
        self.computer.product_tmpl_id.write(
            {
                "renting_min_start_date": "2026-05-26",
                "renting_max_end_date": "2026-05-29",
            }
        )
        self.chainsaw.product_tmpl_id.write(
            {
                "renting_min_start_date": False,
                "renting_max_end_date": False,
            }
        )

        so = self.make_so()
        self.assertFalse(so._can_rent_this_product(self.chainsaw))

    @freeze_time("2026, 1, 1")
    def test_allowed_to_rent_02(self):
        self.computer.product_tmpl_id.write(
            {
                "renting_min_start_date": False,
                "renting_max_end_date": False,
            }
        )
        self.chainsaw.product_tmpl_id.write(
            {
                "renting_min_start_date": False,
                "renting_max_end_date": False,
            }
        )

        so = self.make_so()
        self.assertTrue(so._can_rent_this_product(self.chainsaw))

    @freeze_time("2026, 1, 1")
    def test_allowed_to_rent_03(self):
        self.computer.product_tmpl_id.write(
            {
                "renting_min_start_date": False,
                "renting_max_end_date": False,
            }
        )
        self.chainsaw.product_tmpl_id.write(
            {
                "renting_min_start_date": "2026-05-26",
                "renting_max_end_date": "2026-05-29",
            }
        )

        so = self.make_so()
        self.assertFalse(so._can_rent_this_product(self.chainsaw))

    @freeze_time("2026, 1, 1")
    def test_allowed_to_rent_04(self):
        same_min_start_date = "2026-05-26"
        same_max_end_date = "2026-05-29"
        self.computer.product_tmpl_id.write(
            {
                "renting_min_start_date": same_min_start_date,
                "renting_max_end_date": same_max_end_date,
            }
        )
        self.chainsaw.product_tmpl_id.write(
            {
                "renting_min_start_date": same_min_start_date,
                "renting_max_end_date": same_max_end_date,
            }
        )

        so = self.make_so()
        self.assertTrue(so._can_rent_this_product(self.chainsaw))

    @freeze_time("2026, 1, 1")
    def test_allowed_to_rent_05(self):
        self.computer.product_tmpl_id.write(
            {
                "renting_min_start_date": "2026-05-27",
                "renting_max_end_date": "2026-05-29",
            }
        )
        self.chainsaw.product_tmpl_id.write(
            {
                "renting_min_start_date": "2026-05-26",  # this differs
                "renting_max_end_date": "2026-05-29",
            }
        )

        so = self.make_so()
        self.assertFalse(so._can_rent_this_product(self.chainsaw))
