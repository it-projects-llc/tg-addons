from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestWebsiteResetPassword(HttpCase):
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
