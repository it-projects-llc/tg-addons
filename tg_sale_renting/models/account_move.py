from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _invoice_paid_hook(self):
        res = super()._invoice_paid_hook()
        self.mapped("invoice_line_ids.sale_line_ids.order_id")._compute_payment_status()
        return res
