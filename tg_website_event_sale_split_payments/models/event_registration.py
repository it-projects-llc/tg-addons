from odoo import fields, models
from odoo.tools import float_compare


class EventRegistration(models.Model):
    _inherit = "event.registration"

    is_fully_paid = fields.Boolean(compute="_compute_is_fully_paid")

    def _compute_is_fully_paid(self):
        for record in self:
            order = record.sale_order_id
            if not order:
                record.is_fully_paid = True
            elif not order.invoice_plan_ids:
                record.is_fully_paid = True
            else:
                record.is_fully_paid = (
                    float_compare(
                        order.amount_total,
                        sum(
                            order.mapped("invoice_plan_ids.invoice_move_ids").mapped(
                                lambda x: x.amount_total
                                if x.payment_state in ("paid", "in_payment")
                                else 0
                            )
                        ),
                        precision_rounding=order.currency_id.rounding,
                    )
                    <= 0
                )
