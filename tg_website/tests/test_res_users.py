from odoo.tests.common import TransactionCase

from odoo.addons.website.tools import MockRequest


class TestWebsiteResUsers(TransactionCase):
    def _create_user_via_website(self, website, login):
        # We need a fake request to _signup_create_user.
        with MockRequest(self.env, website=website):
            return (
                self.env["res.users"]
                .with_context(website_id=website.id)
                ._signup_create_user(
                    {
                        "name": login,
                        "login": login,
                    }
                )
            )

    def test_multi_website_multi_company_01(self):
        company_1 = self.env["res.company"].create({"name": "Company 1"})
        company_2 = self.env["res.company"].create({"name": "Company 2"})
        website = self.env["website"].create(
            {
                "name": "Website 1",
                "company_id": company_1.id,
                "auth_signup_uninvited": "b2c",
            }
        )

        self.env.ref("base.template_portal_user_id").company_ids |= company_2

        user = self._create_user_via_website(website, "user1")
        self.assertIn(company_1, user.company_ids)
        self.assertIn(company_2, user.company_ids)
