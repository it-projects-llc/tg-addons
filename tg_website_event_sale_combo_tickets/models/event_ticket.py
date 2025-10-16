from odoo import fields, models


class EventTemplateTicket(models.Model):
    _inherit = "event.type.ticket"

    include_accomodation = fields.Boolean("Navigate to accomodation")
