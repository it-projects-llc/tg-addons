from freezegun import freeze_time

from odoo.tests import HttpCase

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_sale_renting.tests.common import TestWebsiteSaleRentingCommon


class TestMisc(HttpCase, TestWebsiteSaleRentingCommon):
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
