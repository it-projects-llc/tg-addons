from datetime import timedelta

from odoo import fields, models

from ..const import DEFAULT_MAX_INSTALLMENT_DATE


class Company(models.Model):
    _inherit = "res.company"

    invoice_plan_min_deposit_percent = fields.Float(
        compute="_compute_split_payment_values", compute_sudo=True
    )
    invoice_plan_max_deposit_percent = fields.Float(
        compute="_compute_split_payment_values", compute_sudo=True
    )
    invoice_plan_min_deposit_abs = fields.Float(
        compute="_compute_split_payment_values", compute_sudo=True
    )
    invoice_plan_security_days = fields.Integer(
        compute="_compute_split_payment_values", compute_sudo=True
    )
    invoice_plan_max_installment_date = fields.Date(
        compute="_compute_split_payment_values", compute_sudo=True
    )

    def _compute_split_payment_values(self):
        get_param = self.env["ir.config_parameter"].get_param

        def gp(p, d):
            return get_param(f"tg_website_event_sale_split_payments.{p}", d)

        min_deposit_percent = float(gp("invoice_plan_min_deposit_percent", 0))
        max_deposit_percent = float(gp("invoice_plan_max_deposit_percent", 0))
        min_deposit_abs = float(gp("invoice_plan_min_deposit_abs", 0))
        last_installment_date = gp("last_installment_date", False)
        security_days = int(gp("security_days", 0))

        if not last_installment_date:
            last_installment_date = DEFAULT_MAX_INSTALLMENT_DATE
        else:
            last_installment_date = fields.Date.to_date(
                last_installment_date
            ) - timedelta(days=security_days)

        for record in self:
            record.invoice_plan_min_deposit_percent = min_deposit_percent
            record.invoice_plan_max_deposit_percent = max_deposit_percent
            record.invoice_plan_min_deposit_abs = min_deposit_abs
            record.invoice_plan_max_installment_date = last_installment_date
            record.invoice_plan_security_days = security_days
