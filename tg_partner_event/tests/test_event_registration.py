from odoo.addons.partner_event.tests.test_event_registration import (
    TestEventRegistration as Base,
)

Base.__unittest_skip__ = True


class TestEventRegistration(Base):
    __unittest_skip__ = False

    def test_allow_to_change_attendee_partner(self):
        partner2 = self.env["res.partner"].create(
            {
                "name": "Test Partner 222",
                "email": "email222@test.com",
            }
        )

        reg = self.env["event.registration"].create(
            {
                "attendee_partner_id": partner2.id,
                "event_id": self.event_0.id,
            }
        )

        partner2.with_context(
            allow_attendee_partner_change=True
        ).email = self.partner_01.email

        # original partner_event behavior
        # change email to email for existing partner - it will be rewritten
        self.assertNotEqual(reg.attendee_partner_id, partner2)

    def test_no_change_attendee_partner(self):
        partner2 = self.env["res.partner"].create(
            {
                "name": "Test Partner 222",
                "email": "email222@test.com",
            }
        )

        reg = self.env["event.registration"].create(
            {
                "attendee_partner_id": partner2.id,
                "event_id": self.event_0.id,
            }
        )

        partner2.email = self.partner_01.email
        self.assertEqual(reg.attendee_partner_id, partner2)
