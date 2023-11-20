from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        record = super(SaleOrder, self).create(vals)
        # TODO: не применяется
        record.code_promo_program_id = record.affiliate_request_id.affiliate_id.code_promo_program_id
        record.recompute_coupon_lines()
        return record
