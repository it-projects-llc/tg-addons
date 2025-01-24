from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _try_apply_code(self, code):
        self.ensure_one()

        SaleAffiliate = self.sudo().env["sale.affiliate"]
        affiliate = SaleAffiliate.search([("promo_code", "=", code)], limit=1)

        if affiliate:
            self.affiliate_request_id = affiliate.get_request()
            promo = affiliate.code_promo_program_id
            if promo:
                # apply code from first rule
                code = promo.rule_ids.filtered(lambda x: x.code)[:1].code

        return super()._try_apply_code(code)
