from odoo.tests.common import TransactionCase, new_test_user


class TestPartnerLogins(TransactionCase):
    def test_logins_for_single_user(self):
        user = new_test_user(self.env, "partner-logins-single@example.com")

        self.assertEqual(user.partner_id.logins, user.login)

    def test_logins_for_multiple_users_are_sorted(self):
        partner = self.env["res.partner"].create({"name": "Partner with users"})
        new_test_user(
            self.env,
            "z-partner-logins@example.com",
            partner_id=partner.id,
        )
        new_test_user(
            self.env,
            "a-partner-logins@example.com",
            partner_id=partner.id,
        )

        self.assertEqual(
            partner.logins,
            "a-partner-logins@example.com, z-partner-logins@example.com",
        )
