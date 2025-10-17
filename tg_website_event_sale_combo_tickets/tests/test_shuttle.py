from datetime import timedelta

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_event_sale.tests.common import TestWebsiteEventSaleCommon


class TestShuttle(TestWebsiteEventSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        shuttle_date = cls.event.date_begin - timedelta(days=1)

        cls.shuttle_event = cls.env["event.event"].create(
            {
                "name": "ShuttleTestEvent",
                "date_begin": shuttle_date,
                "date_end": shuttle_date,
                "date_tz": cls.event.date_tz,
            }
        )

        cls.ticket_with_shuttle = cls.env["event.event.ticket"].create(
            {
                "event_id": cls.event.id,
                "name": "Ticket with shuttle",
                "product_id": cls.product_event.id,
                "price": 200,
            },
        )

        cls.shuttle_ticket1 = cls.env["event.event.ticket"].create(
            {
                "name": "ShuttleTestTicket1",
                "event_id": cls.shuttle_event.id,
            }
        )

        cls.shuttle_ticket2 = cls.env["event.event.ticket"].create(
            {
                "name": "ShuttleTestTicket2",
                "event_id": cls.shuttle_event.id,
            }
        )

        cls.event_question_name = cls.env["event.question"].create(
            {
                "title": "Name",
                "question_type": "name",
                "event_id": cls.event.id,
            }
        )

        cls.event_question_shuttle_1 = cls.env["event.question"].create(
            {
                "title": "Shuttle Event 1",
                "question_type": "simple_choice",
                "event_id": cls.event.id,
                "is_shuttle_ticket": True,
                "restricted_ticket_ids": [
                    (5,),
                    (4, cls.ticket_with_shuttle.id),
                ],
                "answer_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "ShuttleTicketAnswer1",
                            "shuttle_ticket": cls.shuttle_ticket1.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "ShuttleTicketAnswer2",
                            "shuttle_ticket": cls.shuttle_ticket2.id,
                        },
                    ),
                ],
            }
        )

    def test_shuttle_registration(self):
        event = self.event
        name_question = self.event_question_name
        shuttle_question = self.event_question_shuttle_1

        form_details = {
            "1-name-%s" % name_question.id: "Alyx",
            "1-simple_choice-%s" % shuttle_question.id: str(
                shuttle_question.answer_ids[0].id
            ),
            "1-event_ticket_id": self.ticket_with_shuttle.id,
            "2-name-%s" % name_question.id: "Gordon",
            "2-event_ticket_id": self.ticket.id,
        }

        with MockRequest(self.env, website=self.current_website):
            c = WebsiteEventController()
            registration_data = c._process_attendees_form(event, form_details)
            registrations = c._create_attendees_from_registration_post(
                event, registration_data
            )

        self.assertEqual(len(registrations), 2)

        reg_with_shuttle = registrations.filtered(
            lambda x: x.event_ticket_id == self.ticket_with_shuttle
        )
        reg_without_shuttle = registrations.filtered(
            lambda x: x.event_ticket_id == self.ticket
        )
        self.assertEqual(len(reg_with_shuttle.shuttle_regs), 1)
        self.assertEqual(len(reg_without_shuttle.shuttle_regs), 0)

        shuttle_reg = reg_with_shuttle.shuttle_regs
        self.assertEqual(shuttle_reg.event_id, self.shuttle_event)
        self.assertEqual(shuttle_reg.event_ticket_id, self.shuttle_ticket1)
