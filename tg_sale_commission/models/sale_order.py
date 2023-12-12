from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ui_hide_commission_fields = fields.Boolean(compute="_compute_ui", store=False)

    def _compute_ui(self):
        for record in self:
            record.ui_hide_commission_fields = bool(
                record.company_id.commission_settlement_company
            )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("order_id.affiliate_request_id")
    def _compute_agent_ids(self):
        self.agent_ids = False
        affiliated_order_lines = self.filtered(
            lambda x: x.order_id.affiliate_request_id
            and (x.event_ok or x.is_reward_line)
        )
        for line in affiliated_order_lines:
            agent = line.order_id.affiliate_request_id.affiliate_id.partner_id
            if not agent.commission_id:
                continue
            if not line.commission_free:
                line.agent_ids = [(0, 0, self._prepare_agent_vals(agent))]
