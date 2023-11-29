from odoo import api, models


class AccountInvoiceLineAgent(models.Model):
    _inherit = "account.invoice.line.agent"

    @api.depends("object_id", "object_id.company_id")
    def _compute_company(self):
        super(AccountInvoiceLineAgent, self)._compute_company()
        return
        for line in self:
            if line.company_id.commission_settlement_company:
                line.company_id = line.company_id.commission_settlement_company
