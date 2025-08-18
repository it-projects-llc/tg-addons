from odoo import fields, models


class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    are_happy_hours_enabled = fields.Boolean()
    happy_hours_monday = fields.Boolean("Monday")
    happy_hours_tuesday = fields.Boolean("Tuesday")
    happy_hours_wednesday = fields.Boolean("Wednesday")
    happy_hours_thursday = fields.Boolean("Thursday")
    happy_hours_friday = fields.Boolean("Friday")
    happy_hours_saturday = fields.Boolean("Saturday")
    happy_hours_sunday = fields.Boolean("Sunday")
    happy_hours_from = fields.Float()
    happy_hours_to = fields.Float()
