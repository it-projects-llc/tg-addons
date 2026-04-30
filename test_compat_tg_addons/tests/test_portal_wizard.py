from odoo.tests.common import TransactionCase

from odoo.addons.auth_signup.models.res_users import SignupError


class TestPortalWizard(TransactionCase):
    def test_portal_wizard_email_partner_check(self):
        self.env.company.partner_email_check_filter_duplicates = False

        partner1, partner2 = self.env["res.partner"].create(
            [
                {
                    "name": "Test Partner 1",
                    "email": "test_dup@mail.com",
                },
                {
                    "name": "Test Partner 2",
                    "email": "test_dup@mail.com",
                },
            ]
        )

        self.env.company.partner_email_check_filter_duplicates = True
        with self.assertRaises(SignupError):
            partner1._check_email_unique()

        portal_wizard = (
            self.env["portal.wizard"].with_context(active_ids=[partner1.id]).create({})
        )
        portal_wizard.user_ids._create_user()

        self.assertTrue(partner1.user_ids)
