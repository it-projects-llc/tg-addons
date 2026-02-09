from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_tz(self):
        return "America/Panama"
