from odoo import _, api, models
from odoo.exceptions import UserError


class Settlement(models.Model):
    _inherit = "sale.commission.settlement"

    def name_get(self):
        res = []
        for record in self:
            name = _("Settlement for %s (%s - %s)") % (
                record.agent_id.name,
                record.date_from,
                record.date_to,
            )
            res.append((record.id, name))
        return res


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
