from odoo import api, fields, models


class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    are_happy_hours_enabled = fields.Boolean(
        compute="_compute_are_happy_hours_enabled", store=True, readonly=False
    )
    happy_hours_monday = fields.Boolean("Mon")
    happy_hours_tuesday = fields.Boolean("Tue")
    happy_hours_wednesday = fields.Boolean("Wed")
    happy_hours_thursday = fields.Boolean("Thu")
    happy_hours_friday = fields.Boolean("Fri")
    happy_hours_saturday = fields.Boolean("Sat")
    happy_hours_sunday = fields.Boolean("Sun")
    happy_hours_from = fields.Float()
    happy_hours_to = fields.Float()

    @api.depends("program_type", "pos_ok")
    def _compute_are_happy_hours_enabled(self):
        for program in self:
            if program.program_type != "promotion" or not program.pos_ok:
                program.are_happy_hours_enabled = False
