from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_price_total_using_max_tier_price(self):
        self.ensure_one()
        if self.event_ticket_id.max_tier_price:
            return self.product_uom_qty * self.event_ticket_id.max_tier_price
        else:
            return self.price_total
