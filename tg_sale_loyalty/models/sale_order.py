from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _try_apply_code(self, code):
        if isinstance(code, str):
            code = code.strip()
        return super()._try_apply_code(code)
