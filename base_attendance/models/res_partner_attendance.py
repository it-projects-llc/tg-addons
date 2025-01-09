from odoo import fields, models


class PartnerAttendance(models.Model):
    _name = "res.partner.attendance"
    _description = "Partner Attendance"
    _order = "check_in desc"

    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="cascade", index=True
    )
    check_in = fields.Datetime(required=True)
    check_out = fields.Datetime()
    worked_hours = fields.Float(readonly=True)
    new_id = fields.Many2one("hr.attendance")
