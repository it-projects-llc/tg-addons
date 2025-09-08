from datetime import timedelta

from odoo import api, fields, models


class Event(models.Model):
    _inherit = "event.event"

    max_installment_date = fields.Date(
        compute="_compute_max_installment_date", compute_sudo=True
    )

    @api.depends("company_id")
    def _compute_max_installment_date(self):
        for event in self:
            event.max_installment_date = fields.Date.to_date(
                event.date_begin
            ) - timedelta(days=event.company_id.invoice_plan_security_days)
