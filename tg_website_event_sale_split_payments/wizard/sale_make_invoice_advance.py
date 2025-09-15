from collections import defaultdict

from odoo import models
from odoo.tools import float_round


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, so_lines):
        res = super()._prepare_invoice_values(order, so_lines)
        if not self.env.context.get("invoice_plan_id") and any(
            [not x.is_downpayment for x in so_lines]
        ):
            return res

        rounding = order.currency_id.rounding

        accounts_with_qty = defaultdict(float)
        sum_qty = 0

        for line in order.order_line:
            if line.display_type:
                continue

            if line.is_downpayment:
                continue

            product = line.product_id
            account = product._get_product_accounts()["income"]
            qty = line._get_price_total_using_max_tier_price()
            accounts_with_qty[account] += qty
            sum_qty += qty

        if not accounts_with_qty:
            return res

        accounts_with_weights = {}
        sum_rounded = 0.0

        last_account = list(accounts_with_qty.keys())[-1]
        for k, v in accounts_with_qty.items():
            if k == last_account:
                continue
            accounts_with_weights[k] = float_round(
                v / sum_qty, precision_rounding=rounding
            )
            sum_rounded += accounts_with_weights[k]

        accounts_with_weights[last_account] = float_round(
            1 - sum_rounded, precision_rounding=rounding
        )

        original_invoice_lines = res.pop("invoice_line_ids")

        new_invoice_lines = []
        for account, weight in accounts_with_weights.items():
            for oil in original_invoice_lines:
                x = oil[2].copy()
                x["quantity"] = weight
                x["account_id"] = account.id
                new_invoice_lines.append((0, 0, x))

        res["invoice_line_ids"] = new_invoice_lines
        return res
