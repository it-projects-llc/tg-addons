from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount_total_with_agents = fields.Monetary(
        string="Total with agents", compute="_compute_total_with_agents"
    )
    ui_hide_commission_fields = fields.Boolean(compute="_compute_ui", store=False)

    def _compute_ui(self):
        for record in self:
            record.ui_hide_commission_fields = bool(
                record.company_id.commission_settlement_company
            )

    def _compute_total_with_agents(self):
        for record in self:
            order_line = record.order_line
            record.amount_total_with_agents = sum(
                order_line.filtered("agent_ids").mapped("price_total")
            )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("order_id.affiliate_request_id")
    def _compute_agent_ids(self):
        self.agent_ids = False
        affiliated_order_lines = self.filtered(lambda x: x._is_affiliated_order_line())
        for line in affiliated_order_lines:
            agent = line.order_id.affiliate_request_id.affiliate_id.partner_id
            if not agent.commission_id:
                continue
            if not line.commission_free:
                line.agent_ids = [(0, 0, self._prepare_agent_vals(agent))]

    def _is_affiliated_order_line(self):
        return bool(self.order_id.affiliate_request_id)
