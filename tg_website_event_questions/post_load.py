def post_load():
    from odoo.addons.website_event_questions.controllers.main import (
        WebsiteEvent,
        request,
    )

    def _process_attendees_form(self, event, form_details):
        """ Process data posted from the attendee details form.
        Extracts question answers:
        - For both questions asked 'once_per_order' and questions asked to every attendee
        - For questions of type 'simple_choice', extracting the suggested answer id
        - For questions of type 'text_box', extracting the text answer of the attendee. """
        registrations = super(WebsiteEvent, self)._process_attendees_form(event, form_details)

        for registration in registrations:
            registration['registration_answer_ids'] = []

        general_answer_ids = []
        for key, value in form_details.items():
            if 'question_answer' in key and value:
                dummy, registration_index, question_id = key.split('-')
                question_sudo = request.env['event.question'].browse(int(question_id))
                answer_values = None
                if question_sudo.question_type == 'simple_choice' and not question_sudo.is_marketing:  # <-- changed here
                    answer_values = {
                        'question_id': int(question_id),
                        'value_answer_id': int(value)
                    }
                # changes start
                elif question_sudo.question_type == 'simple_choice' and question_sudo.is_marketing:
                    try:
                        value_answer_id = int(value)
                        value_answer = request.env['event.question.answer'].sudo().browse(value_answer_id).exists()

                        if not value_answer:
                            raise ValueError()
                        if value_answer.question_id.id != question_sudo.id:
                            raise ValueError()

                        answer_values = {
                            'question_id': int(question_id),
                            'value_answer_id': value_answer_id,
                        }

                    except (IndexError, ValueError):
                        answer_values = {
                            'question_id': int(question_id),
                            'value_text_box': value
                        }
                # changes end
                elif question_sudo.question_type == 'text_box':
                    answer_values = {
                        'question_id': int(question_id),
                        'value_text_box': value
                    }

                if answer_values and not int(registration_index):
                    general_answer_ids.append((0, 0, answer_values))
                elif answer_values:
                    registrations[int(registration_index) - 1]['registration_answer_ids'].append((0, 0, answer_values))

        for registration in registrations:
            registration['registration_answer_ids'].extend(general_answer_ids)

        return registrations

    WebsiteEvent._process_attendees_form = _process_attendees_form
