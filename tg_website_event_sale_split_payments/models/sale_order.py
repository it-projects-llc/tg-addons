from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Date
from odoo.tools import float_is_zero, format_amount, format_date


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

        if not self.order_line:
            return self.company_id.invoice_plan_max_installment_date

        return min(self.order_line.mapped(lambda x: x._get_max_installment_date()))

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
                is_first_plan = plan == self.invoice_plan_ids[0]
                is_last_plan = plan == self.invoice_plan_ids[-1]
                MakeInvoice = self.sudo().env["sale.advance.payment.inv"]
                makeinvoice = MakeInvoice.create(
                    {
                        "advance_payment_method": "fixed",
                        "fixed_amount": plan.amount,
                        "sale_order_ids": [(6, 0, self.ids)],
                    }
                )

                require_account_sums = None

                if is_last_plan:
                    require_account_sums = defaultdict(float)
                    income_accounts_for_so = self._calculate_income_accounts()
                    income_accounts_from_invoices = self.mapped(
                        "invoice_plan_ids.invoice_move_ids"
                    )._calculate_accounts()

                    for account, invoice_sum in income_accounts_from_invoices.items():
                        require_account_sums[account] = (
                            income_accounts_for_so[account] - invoice_sum
                        )

                makeinvoice.sudo().with_context(
                    name_as_installment=not is_first_plan,
                    invoice_plan_id=plan.id,
                    mail_auto_subscribe_no_notify=True,
                    require_account_sums=require_account_sums,
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
                "require_payment": False,
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
            total_with_max_tier += line._get_price_total_using_max_tier_price()

        return total_with_max_tier

    def _calculate_income_accounts(self):
        self.ensure_one()
        res = defaultdict(float)

        currency_rounding = self.currency_id.rounding

        for line in self.order_line:
            if line.display_type:
                continue

            if line.is_downpayment:
                continue

            qty = line._get_price_total_using_max_tier_price()
            if float_is_zero(qty, precision_rounding=currency_rounding):
                continue

            product = line.product_id
            account = product._get_product_accounts()["income"]
            res[account] += qty

        return res
