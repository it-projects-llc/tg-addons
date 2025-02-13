import json

from odoo.http import content_disposition, request, route

from odoo.addons.event.controllers.main import EventController


class EventControllerExtended(EventController):
    @route()
    def event_my_tickets(self, event_id, registration_ids, tickets_hash):
        super().event_my_tickets(event_id, registration_ids, tickets_hash)

        event = request.env["event.event"].browse(event_id)
        event_sudo = event.exists().sudo()
        event_registrations_sudo = event_sudo.registration_ids.filtered(
            lambda reg: reg.id in json.loads(registration_ids or "[]")
        )

        default_xml_id = "event.action_report_event_registration_badge"
        if event.report_template_for_portal:
            xml_id = event_sudo.report_template_for_portal.get_metadata()[0].get(
                "xmlid"
            )
        if not xml_id:
            xml_id = default_xml_id

        pdf = (
            request.env["ir.actions.report"]
            .sudo()
            ._render_qweb_pdf(
                xml_id,
                event_registrations_sudo.ids,
            )[0]
        )
        pdfhttpheaders = [
            ("Content-Type", "application/pdf"),
            ("Content-Length", len(pdf)),
            (
                "Content-Disposition",
                content_disposition(
                    f"Tickets-{event_sudo.name} ({event_sudo.date_begin_located}).pdf"
                ),
            ),
        ]
        return request.make_response(pdf, headers=pdfhttpheaders)
