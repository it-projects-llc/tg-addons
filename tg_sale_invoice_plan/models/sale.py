# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_plan_ids = fields.One2many(
        comodel_name="sale.invoice.plan",
        inverse_name="sale_id",
        string="Inovice Plan",
        copy=False,
    )
    use_invoice_plan = fields.Boolean(
        default=False,
        copy=False,
    )
    invoice_plan_process = fields.Boolean(
        string="Invoice Plan In Process",
        compute="_compute_invoice_plan_process",
        help="At least one invoice plan line pending to create invoice",
    )
    invoice_plan_total_amount = fields.Monetary(
        compute="_compute_invoice_plan_total",
        string="Total Amount",
    )

    @api.depends("invoice_plan_ids")
    def _compute_invoice_plan_total(self):
        for rec in self:
            installments = rec.invoice_plan_ids
            rec.invoice_plan_total_amount = sum(installments.mapped("amount"))

    def _compute_invoice_plan_process(self):
        for rec in self:
            has_invoice_plan = rec.use_invoice_plan and rec.invoice_plan_ids
            to_invoice = rec.invoice_plan_ids.filtered(lambda line: not line.invoiced)
            inv_or_adv = rec.invoice_status == "to invoice"
            rec.invoice_plan_process = (
                rec.state == "sale" and has_invoice_plan and to_invoice and inv_or_adv
            )

    def action_confirm(self):
        if self.filtered(lambda r: r.use_invoice_plan and not r.invoice_plan_ids):
            raise UserError(_("Use Invoice Plan selected, but no plan created"))
        return super().action_confirm()

    def _create_invoice_plan(
        self,
        num_installment,
        installment_date,
        interval,
        interval_type,
        first_amount,
        amount_total,
    ):
        self.ensure_one()
        self.invoice_plan_ids.unlink()
        invoice_plans = []

        if first_amount:
            vals = {
                "installment": 0,
                "plan_date": installment_date,
                "amount": first_amount,
            }
            invoice_plans.append((0, 0, vals))
            installment_date = self._next_date(
                installment_date, interval, interval_type
            )
            num_installment = num_installment - 1

        ratio = 1.0 / num_installment

        sum_amount = first_amount
        for i in range(num_installment):
            this_installment = i + 1
            if num_installment == this_installment:
                amount = amount_total - sum_amount
            else:
                amount = float_round(
                    ratio * (amount_total - first_amount),
                    precision_rounding=self.currency_id.rounding,
                )
                sum_amount += amount
            vals = {
                "installment": this_installment,
                "plan_date": installment_date,
                "amount": amount,
            }
            invoice_plans.append((0, 0, vals))
            installment_date = self._next_date(
                installment_date, interval, interval_type
            )
        self.write({"invoice_plan_ids": invoice_plans})
        return True

    def remove_invoice_plan(self):
        self.ensure_one()
        self.invoice_plan_ids.unlink()
        return True

    @api.model
    def _next_date(self, installment_date, interval, interval_type):
        installment_date = fields.Date.to_date(installment_date)
        if interval_type == "month":
            next_date = installment_date + relativedelta(months=+interval)
        elif interval_type == "year":
            next_date = installment_date + relativedelta(years=+interval)
        else:
            next_date = installment_date + relativedelta(days=+interval)
        return next_date

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        invoice_plan_id = self._context.get("invoice_plan_id")
        if invoice_plan_id:
            plan = self.env["sale.invoice.plan"].browse(invoice_plan_id)
            for move in moves:
                move.invoice_date = plan.plan_date
            plan.invoice_move_ids += moves
        return moves
