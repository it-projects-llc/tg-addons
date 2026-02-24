from unittest.mock import patch

from odoo.tools.misc import mute_logger

from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.partner_email_check.tests.test_partner_email_check import (
    TestPartnerEmailCheck as Base,
)

Base.__unittest_skip__ = True  # do not run tests of original sale_commission


class TestPartnerEmailCheck(Base):
    __unittest_skip__ = False

    def test_ignore_list_01(self):
        self.disallow_duplicates()

        self.env["partner.email.check.ignore"].create(
            {
                "domain": "testignore.com",
            }
        )

        self.test_partner.email = "mail@testignore.com"
        self.env["res.partner"].create(
            {"name": "alsotest", "email": "mail@testignore.com"}
        )

    # ------------------
    # following methods were copied from original partner_email_check
    # assertRaises param are replaced from UserError to SignupError

    def test_duplicate_addresses_disallowed(self):
        self.disallow_duplicates()
        self.test_partner.write({"email": "email@domain.tld"})
        with self.assertRaises(SignupError):
            self.env["res.partner"].create(
                {"name": "alsotest", "email": "email@domain.tld"}
            )

    def test_duplicate_after_normalization_addresses_disallowed(self):
        self.disallow_duplicates()
        self.env["res.partner"].create(
            {"name": "alsotest", "email": "email@doMAIN.tld"}
        )
        with self.assertRaises(SignupError):
            self.test_partner.email = "email@domain.tld"

    @mute_logger("odoo.addons.partner_email_check.models.res_partner")
    def test_lacking_dependency_keeps_uniqueness_constraint_working(self):
        self.disallow_duplicates()
        with patch(
            "odoo.addons.partner_email_check.models.res_partner." "validate_email", None
        ):
            self.env["res.partner"].create(
                {"name": "alsotest", "email": "email@domain.tld"}
            )
            with self.assertRaises(SignupError):
                self.test_partner.email = "email@domain.tld"
