from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_applicable_no_code_promo_program(self):
        res = self.affiliate_request_id.affiliate_id.code_promo_program_id
        return res + super()._get_applicable_no_code_promo_program()
