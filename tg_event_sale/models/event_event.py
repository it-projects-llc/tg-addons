from odoo import models


class Event(models.Model):
    _inherit = "event.event"

    def _compute_sale_price_subtotal(self):
        for event in self:
            orders = event.sale_order_lines_ids.mapped("order_id").filtered_domain(
                [("state", "!=", "cancel")]
            )
            event.sale_price_subtotal = sum(orders.mapped("amount_total") or [0])
