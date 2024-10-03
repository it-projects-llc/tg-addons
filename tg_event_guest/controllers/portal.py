from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal as BaseCustomerPortal


class CustomerPortal(BaseCustomerPortal):
    @route()
    def account(self, redirect=None, **post):
        if not request.httprequest.method == "POST":
            if post.get("guest_register_code"):
                guest = request.env["event.guest"]._get_by_code(
                    post["guest_register_code"]
                )
                if guest.guest_partner == request.env.user.partner_id:
                    guest.result_partner = request.env.user.partner_id

        res = super(CustomerPortal, self).account(redirect, **post)

        if not request.httprequest.method == "POST":
            # we are handling only POST requests here
            return res

        if res.status_code == 200:
            # some fields are not correct
            return res

        partner = request.env.user.partner_id
        guest = request.env.user.event_guest

        if not guest:
            return res

        if not guest.result_attendee:
            Attendee = request.env["event.registration"].sudo()
            vals = {
                "name": partner.name,
                "event_id": guest.event.id,
                "event_ticket_id": guest.event_ticket.id,
                "partner_id": partner.id,
            }

            # additional field from partner_event
            if "attendee_partner_id" in Attendee._fields:
                vals["attendee_partner_id"] = partner.id

            attendee = Attendee.create(vals)
            attendee.action_confirm()

            ctx = attendee.action_send_badge_email()["context"]
            compose = (
                attendee.env["mail.compose.message"].with_context(**ctx).create({})
            )
            compose.send_mail()
            guest.result_attendee = attendee

        return res
