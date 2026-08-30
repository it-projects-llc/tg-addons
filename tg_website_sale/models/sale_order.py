from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_cart_info(self):
        res = super()._compute_cart_info()
        for order in self:
            order.only_services = True
        return res
