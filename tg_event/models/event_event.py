from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    subscribe_in_registrations = fields.Many2many("res.partner", "event_reg_sub_partner")
