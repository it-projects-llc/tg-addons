from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _is_not_sellable_line(self):
        if self.event_id:
            return True
        return super()._is_not_sellable_line()
