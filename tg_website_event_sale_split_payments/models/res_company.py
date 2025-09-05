from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    invoice_plan_min_deposit_percent = fields.Float(
        compute="_compute_split_payment_values", compute_sudo=True
    )
    invoice_plan_max_deposit_percent = fields.Float(
        compute="_compute_split_payment_values", compute_sudo=True
    )

    def _compute_split_payment_values(self):
        get_param = self.env["ir.config_parameter"].get_param

        def gp(p, d):
            return get_param(f"tg_website_event_sale_split_payments.{p}", d)

        min_deposit_percent = float(gp("invoice_plan_min_deposit_percent", 0))
        max_deposit_percent = float(gp("invoice_plan_max_deposit_percent", 0))
        for record in self:
            record.invoice_plan_min_deposit_percent = min_deposit_percent
            record.invoice_plan_max_deposit_percent = max_deposit_percent
