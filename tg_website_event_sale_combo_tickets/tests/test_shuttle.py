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
            "1-name-%s" % name_question.id: "Eugene",
            "1-simple_choice-%s" % shuttle_question.id: str(
                shuttle_question.answer_ids[0].id
            ),
            "1-event_ticket_id": self.ticket.id,
        }

        with MockRequest(self.env, website=self.current_website):
            c = WebsiteEventController()
            registration_data = c._process_attendees_form(event, form_details)
            registrations = c._create_attendees_from_registration_post(
                event, registration_data
            )

        self.assertTrue(registrations)  # TODO: это лишнее
        # TODO: надо проверить, что shuttle регистрации созданы
