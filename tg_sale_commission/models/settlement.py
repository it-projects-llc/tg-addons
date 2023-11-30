from odoo import _, api, models
from odoo.exceptions import UserError


class SettlementLine(models.Model):
    _inherit = "sale.commission.settlement.line"

    @api.constrains("settlement_id", "agent_line")
    def _check_company(self):
        for record in self:
            for line in record.agent_line:
                if (
                    line.company_id != record.company_id
                    and line.company_id.commission_settlement_company
                    != record.company_id
                ):
                    raise UserError(
                        _("Company must be the same or equal to settlement company")
                    )
