from odoo.tests.common import TransactionCase


class TestEventRegistrations(TransactionCase):
    def test_subscribe_in_registrations(self):
        subscriber_1 = self.env["res.partner"].create({"name": "Subscriber 1"})
        subscriber_2 = self.env["res.partner"].create({"name": "Subscriber 2"})
        attendee = self.env["res.partner"].create({"name": "Test Attendee"})

        event = self.env["event.event"].create(
            {
                "name": "Test Event with Subscribers",
                "subscribe_in_registrations": [
                    (6, 0, [subscriber_1.id, subscriber_2.id])
                ],
            }
        )

        registration = self.env["event.registration"].create(
            {
                "event_id": event.id,
                "partner_id": attendee.id,
                "name": attendee.name,
            }
        )

        subscribed_partner_ids = registration.message_partner_ids.ids

        self.assertIn(subscriber_1.id, subscribed_partner_ids)
        self.assertIn(subscriber_2.id, subscribed_partner_ids)
