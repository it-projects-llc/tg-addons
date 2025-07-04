from odoo.tests import tagged

from odoo.addons.base.tests.common import HttpCaseWithUserPortal


@tagged("post_install", "-at_install")
class TestPortalPassportTour(HttpCaseWithUserPortal):
    def test_portal_passport_tour(self):
        self.start_tour("/my", "tg_portal.portal_passport_tour", login="portal")

        partner = self.partner_portal
        self.assertEqual(partner.passport, "PassportTest")
        self.assertEqual(partner.cedula, "CedulaTest")
        self.assertTrue(partner.has_cedula)
