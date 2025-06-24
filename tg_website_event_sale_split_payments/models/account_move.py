from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _invoice_paid_hook(self):
        res = super()._invoice_paid_hook()

        for invoice in self.filtered(lambda move: move.is_invoice()):
            for order in invoice.mapped("invoice_line_ids.sale_line_ids.order_id"):
                if invoice in order.invoice_plan_ids[
                    :1
                ].invoice_move_ids and order.state in ("draft, sent"):
                    order.action_confirm()

                    for invoice in order.filtered(
                        "auto_confirm_invoices_for_plan"
                    ).mapped("invoice_plan_ids.invoice_move_ids"):
                        if invoice.state != "posted":
                            invoice.action_post()

                    order._send_order_invoice_plan_mail()

        return res
