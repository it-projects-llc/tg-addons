from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
#        AffiliateRequest = self.env["sale.affiliate.request"]
#        res.affiliate_request_id = AffiliateRequest.current_qualified()
        return res
