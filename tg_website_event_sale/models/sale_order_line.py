from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _is_affiliated_order_line(self):
        return (
            self.event_id or self.event_ticket_id or self.is_reward_line
        ) and super()._is_affiliated_order_line()
