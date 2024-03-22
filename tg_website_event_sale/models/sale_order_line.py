from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _is_affiliated_order_line(self):
        return (self.event_ok or self.is_reward_line) and super(
            SaleOrderLine, self
        )._is_affiliated_order_line()
