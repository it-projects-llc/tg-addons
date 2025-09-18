from collections import defaultdict

from odoo import models
from odoo.tools import float_is_zero, float_round


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, so_lines):
        res = super()._prepare_invoice_values(order, so_lines)
        if not self.env.context.get("invoice_plan_id") and any(
            [not x.is_downpayment for x in so_lines]
        ):
            return res

        uom_rounding = self.product_id.uom_id.rounding
        currency_rounding = self.sale_order_ids.currency_id.rounding

        accounts_with_qty = order._calculate_income_accounts()
        if not accounts_with_qty:
            return res

        sum_qty = sum(accounts_with_qty.values())

        accounts_with_weights = {}
        sum_rounded = 0.0

        last_account = list(accounts_with_qty.keys())[-1]
        for k, v in accounts_with_qty.items():
            if k == last_account:
                continue
            accounts_with_weights[k] = float_round(
                v / sum_qty, precision_rounding=uom_rounding
            )
            sum_rounded += accounts_with_weights[k]

        accounts_with_weights[last_account] = float_round(
            1 - sum_rounded, precision_rounding=uom_rounding
        )

        original_invoice_lines = res.pop("invoice_line_ids")

        new_invoice_lines = []
        sum_for_account = defaultdict(float)
        require_account_sums = self.env.context.get("require_account_sums") or {}

        for account, weight in accounts_with_weights.items():
            for oil in original_invoice_lines:
                x = oil[2].copy()
                x["quantity"] = weight
                x["account_id"] = account.id
                sum_for_account[account] += weight * x["price_unit"]
                new_invoice_lines.append((0, 0, x))

        for account, required_sum in require_account_sums.items():
            diff = required_sum - sum_for_account[account]
            if float_is_zero(diff, precision_rounding=currency_rounding):
                continue

            for oil in original_invoice_lines:
                x = oil[2].copy()
                x["quantity"] = 1
                x["account_id"] = account.id
                x["price_unit"] = diff
                x["name"] = "Minor rounding adjustments"
                new_invoice_lines.append((0, 0, x))

        res["invoice_line_ids"] = new_invoice_lines
        return res
