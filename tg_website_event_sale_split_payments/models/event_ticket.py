from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    max_tier_price = fields.Float()
