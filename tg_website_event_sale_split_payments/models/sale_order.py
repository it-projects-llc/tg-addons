from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Date
from odoo.tools import format_amount, format_date


class SaleOrder(models.Model):
    _inherit = "sale.order"

    auto_confirm_invoices_for_plan = fields.Boolean()

    def _get_max_installments(self, interval, interval_type):
        max_installment_date = self._get_max_installment_date()

        max_num_installments = 0
        installment_date = Date.today()
        while installment_date < max_installment_date:
            max_num_installments += 1
            installment_date = self._next_date(
                installment_date, interval, interval_type
            )
        return max_num_installments

    def _get_max_installment_date(self):
        self.ensure_one()

        max_installment_date = self.company_id.invoice_plan_max_installment_date
        security_days = timedelta(days=self.company_id.invoice_plan_security_days)

        for event in self.mapped("order_line.event_id"):
            max_installment_date = min(event.max_installment_date, max_installment_date)

        # TODO: exclude shuttle products

        # we use gettattr here, since I don't want
        # to put enterprise dependency to this module
        has_rented_products = getattr(self, "has_rented_products", False)
        if has_rented_products:
            max_installemnt_date_of_rental = (
                Date.to_date(self.rental_start_date) - security_days
            )
            max_installment_date = min(
                max_installemnt_date_of_rental, max_installment_date
            )

        return max_installment_date

    def _get_allowed_split_payment_periods(self):
        max_installments = {}

        split_payment_periods = self._get_split_payment_periods()
        for k, v in split_payment_periods.items():
            max_installments[k] = self._get_max_installments(
                v["interval"], v["interval_type"]
            )

        for k, v in max_installments.items():
            if v is None:
                split_payment_periods[k]["max_installments"] = 20
            elif v < 2:
                del split_payment_periods[k]
            else:
                split_payment_periods[k]["max_installments"] = max_installments[k]

        return split_payment_periods

    @api.model
    def _get_split_payment_periods(self):
        self.ensure_one()
        return {
            "month": {
                "interval": 1,
                "interval_type": "month",
                "display_name": _("Monthly"),
            },
            "biweekly": {
                "interval": 14,
                "interval_type": "day",
                "display_name": _("Biweekly"),
            },
        }

    def _prepare_first_plan_payment(self):
        for plan in self.invoice_plan_ids:
            if not plan.invoice_move_ids:
                MakeInvoice = self.sudo().env["sale.advance.payment.inv"]
                makeinvoice = MakeInvoice.create(
                    {
                        "advance_payment_method": "fixed",
                        "fixed_amount": plan.amount,
                        "sale_order_ids": [(6, 0, self.ids)],
                    }
                )
                makeinvoice.sudo().with_context(
                    invoice_plan_id=plan.id,
                    mail_auto_subscribe_no_notify=True,
                ).create_invoices()
                plan.invoice_move_ids.invoice_date = plan.plan_date

        invoice = self.invoice_plan_ids[0].invoice_move_ids[:1]
        if invoice.state != "posted":
            invoice.action_post()

        return invoice

    def _generate_invoice_plan_for_event(
        self,
        deposit,
        payment_count,
        period,
    ):
        if not self.amount_total:
            raise UserError(_("No need to create plan for zero price quotation"))

        company = self.company_id

        min_deposit_abs = company.invoice_plan_min_deposit_abs
        if self.amount_total < min_deposit_abs:
            raise UserError(
                _(
                    "Payment splitting not allowed. "
                    "Total amount (%(amount_total)s) is less than minimal absolute deposit amount (%(min_deposit_abs)s)",  # noqa: E501
                    amount_total=format_amount(
                        self.env,
                        self.amount_total,
                        self.currency_id,
                    ),
                    min_deposit_abs=format_amount(
                        self.env, min_deposit_abs, self.currency_id
                    ),
                )
            )

        min_deposit_ratio = company.invoice_plan_min_deposit_percent / 100
        max_deposit_ratio = company.invoice_plan_max_deposit_percent / 100
        min_deposit = max(min_deposit_ratio * self.amount_total, min_deposit_abs)
        max_deposit = max_deposit_ratio * self.amount_total

        if deposit < min_deposit:
            raise UserError(
                _(
                    "Minimal deposit is %s",
                    format_amount(
                        self.env,
                        min_deposit,
                        self.currency_id,
                    ),
                )
            )

        if deposit > max_deposit:
            raise UserError(
                _(
                    "Maximum deposit is %s",
                    format_amount(
                        self.env,
                        max_deposit,
                        self.currency_id,
                    ),
                )
            )

        if payment_count <= 1:
            raise UserError(_("Payment count should be more than 1"))

        interval_pairs = self._get_split_payment_periods()
        if period not in interval_pairs:
            raise UserError(_("Incorrect period %s", period))

        self.with_context(mail_auto_subscribe_no_notify=True)._create_invoice_plan(
            payment_count,
            Date.today(),
            interval_pairs[period]["interval"],
            interval_pairs[period]["interval_type"],
            deposit,
            self._calculate_amount_total_with_additional_fee(),
        )

        last_plan_date = max(self.invoice_plan_ids.mapped("plan_date"))
        max_installment_date = self._get_max_installment_date()

        if last_plan_date > max_installment_date:
            raise UserError(
                _(
                    "Last payment date (%(last_plan_date)s) exceeds max allowed installment date (%(max_installment_date)s)",  # noqa: E501
                    last_plan_date=format_date(self.env, last_plan_date),
                    max_installment_date=format_date(self.env, max_installment_date),
                )
            )

        self.write(
            {
                "use_invoice_plan": True,
                "auto_confirm_invoices_for_plan": True,
            }
        )

    def _send_order_invoice_plan_mail(self):
        for order in self.filtered("invoice_plan_ids"):
            mail_template = self.env.ref(
                "tg_website_event_sale_split_payments.mail_template_invoice_plan",
                raise_if_not_found=False,
            )
            order._send_order_notification_mail(mail_template)

    def _calculate_additional_fee_for_splitting(self, deposit):
        return max(
            self._calculate_amount_total_with_additional_fee() - self.amount_total, 0
        )

    def _calculate_amount_total_with_additional_fee(self):
        self.ensure_one()

        total_with_max_tier = 0
        for line in self.order_line:
            if line.event_ticket_id.max_tier_price:
                total_with_max_tier += (
                    line.product_uom_qty * line.event_ticket_id.max_tier_price
                )
            else:
                total_with_max_tier += line.price_total

        return total_with_max_tier
