from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _program_check_compute_points(self, programs):
        res = super()._program_check_compute_points(programs)
        affiliate_promo_program = (
            self.affiliate_request_id.affiliate_id.code_promo_program_id
        )
        for program in programs:
            if program not in res:
                # should not happen
                continue

            if "error" in res[program]:
                continue

            if program.only_affiliate_usage:
                if program != affiliate_promo_program:
                    res[program]["error"] = _("This should be applied via affiliate")

        return res

    def _try_apply_code(self, code):
        self.ensure_one()

        SaleAffiliate = self.sudo().env["sale.affiliate"]
        affiliate = SaleAffiliate.search([("promo_code", "=", code)], limit=1)

        if affiliate:
            self.affiliate_request_id = affiliate.get_request()
            return {}

        return super()._try_apply_code(code)
