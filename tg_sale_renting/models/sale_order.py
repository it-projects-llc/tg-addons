from odoo import api, fields, models
from odoo.tools import float_is_zero


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_status = fields.Selection(
        [
            ("not_rental_order", "Not rental order"),
            ("not_paid", "Not Paid"),
            ("partial", "Partially Paid"),
            ("paid", "Paid"),
        ],
        compute="_compute_payment_status",
        store=True,
    )

    @api.depends(
        "is_rental_order",
        "amount_total",
        "currency_id",
        "order_line.invoice_lines.move_id.amount_residual",
    )
    def _compute_payment_status(self):
        for order in self:
            if not order.is_rental_order:
                # для избежаний излишних вычислений
                # особенно при установке модуля
                order.payment_status = "not_rental_order"
                continue

            if float_is_zero(
                order.amount_total, precision_rounding=order.currency_id.rounding
            ):
                order.payment_status = "paid"
                continue

            moves = order.mapped("order_line.invoice_lines.move_id").filtered(
                lambda x: x.state != "cancel"
            )
            payments = moves._get_reconciled_payments().filtered_domain(
                [("source_payment_id", "=", False)]
            )
            amounts = []
            for payment in payments:
                amounts.append(
                    payment.currency_id._convert(
                        payment.amount,
                        order.currency_id,
                        order.company_id,
                        payment.date,
                    )
                )

            amount_paid = sum(amounts)
            if order.currency_id.is_zero(amount_paid):
                order.payment_status = "not_paid"

            elif (
                order.currency_id.compare_amounts(amount_paid, order.amount_total) == -1
            ):
                order.payment_status = "partial"

            else:
                order.payment_status = "paid"
