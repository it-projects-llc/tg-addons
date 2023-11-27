from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("order_id.affiliate_request_id")
    def _compute_agent_ids(self):
        self.agent_ids = False
        affiliated_order_lines = self.filtered(
            lambda x: x.order_id.affiliate_request_id
        )
        for line in affiliated_order_lines:
            agent = line.order_id.affiliate_request_id.affiliate_id.partner
            if not line.commission_free:
                line.agent_ids = [(0, 0, self._prepare_agent_vals(agent))]
