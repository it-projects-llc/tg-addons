from datetime import datetime, timedelta

from odoo import fields
from odoo.tests import TransactionCase


class TestMain(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env["res.config.settings"].create(
            {
                "auth_signup_uninvited": "b2c",
            }
        ).execute()

        cls.Users = cls.env["res.users"].with_context(
            mail_create_nolog=True,
            mail_create_nosubscribe=True,
            mail_notrack=True,
            no_reset_password=True,
        )

        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": fields.Datetime.to_string(
                    datetime.today() + timedelta(days=1)
                ),
                "date_end": fields.Datetime.to_string(
                    datetime.today() + timedelta(days=15)
                ),
                "event_ticket_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test ticket",
                        },
                    )
                ],
            }
        )

    def test_signup_01(self):
        Users = self.Users
        event = self.event

        guest = self.env["event.guest"].create(
            {
                "name": "Eugene",
                "email": "eugene@mailforspam.com",
                "event": event.id,
                "event_ticket": event.event_ticket_ids[0].id,
            }
        )

        guest_user_tuple = Users.signup(
            {
                "name": "eugene1",
                "login": "eugene1",
                "password": "eugene1",
                "guest_register_code": guest.code,
            }
        )
        guest_user = Users.search([("login", "=", guest_user_tuple[1])])

        guest = self.env["event.guest"].browse(guest.id)
        self.assertEqual(guest.result_partner, guest_user.partner_id)

        # for example, some reason other test user registered with already used guest code # noqa: E501

        guest_user_tuple = Users.signup(
            {
                "name": "eugene2",
                "login": "eugene2",
                "password": "eugene2",
                "guest_register_code": guest.code,
            }
        )
        accident_guest_user = Users.search([("login", "=", guest_user_tuple[1])])

        guest = self.env["event.guest"].browse(guest.id)
        self.assertNotEqual(guest.result_partner, accident_guest_user.partner_id)
        self.assertEqual(guest.result_partner, guest_user.partner_id)

    def test_signup_02_has_partner_no_user(self):
        event = self.event

        partner = self.env["res.partner"].create(
            {
                "name": "Eugene",
                "email": "eugene@mailforspam.com",
            }
        )

        guest = self.env["event.guest"].create(
            {
                "name": "Eugene",
                "email": partner.email,
                "event": event.id,
                "event_ticket": event.event_ticket_ids[0].id,
            }
        )
        self.assertEqual(guest.guest_partner, partner)

        # first invite_url must be calculated
        self.assertTrue(guest.invite_url)

        # then partner will have token
        self.assertIn("&token=" + guest.guest_partner.signup_token, guest.invite_url)
