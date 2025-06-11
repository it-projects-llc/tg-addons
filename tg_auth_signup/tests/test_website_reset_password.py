from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.mail.tests.common import MockEmail


@tagged("post_install", "-at_install")
class TestWebsiteResetPassword(HttpCase, MockEmail):
    def test_multi_website_signup_url_different_domain(self):
        website_1, website_2 = self.env["website"].create(
            [
                {"name": "Website 1", "domain": "http://example1.com"},
                {"name": "Website 2", "domain": "http://example2.com"},
            ]
        )

        login = "user@example.com"
        user = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {"login": login, "email": login, "name": login},
            )
        )

        self.assertTrue(
            user.with_context(website_id=website_1.id).signup_url.startswith(
                "http://example1.com"
            )
        )
        self.assertTrue(
            user.with_context(website_id=website_2.id).signup_url.startswith(
                "http://example2.com"
            )
        )

    def test_multi_website_multi_company_email_from(self):
        company_1, company_2 = self.env["res.company"].create(
            [
                {"name": "Company 1", "email": "email@company1.com"},
                {"name": "Company 2", "email": "email@company2.com"},
            ]
        )
        website_1, website_2 = self.env["website"].create(
            [
                {
                    "name": "Website 1",
                    "domain": "http://example1.com",
                    "company_id": company_1.id,
                },
                {
                    "name": "Website 2",
                    "domain": "http://example2.com",
                    "company_id": company_2.id,
                },
            ]
        )

        login = "user@example.com"
        user = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {"login": login, "email": login, "name": login},
            )
        )

        with self.mock_mail_gateway():
            user.with_context(website_id=website_1.id).action_reset_password()
        self.assertEqual(self._mails[-1]["email_from"], company_1.email_formatted)

        with self.mock_mail_gateway():
            user.with_context(website_id=website_2.id).action_reset_password()
        self.assertEqual(self._mails[-1]["email_from"], company_2.email_formatted)
