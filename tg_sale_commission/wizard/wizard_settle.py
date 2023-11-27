from odoo import models


class SaleCommissionMakeSettle(models.TransientModel):
    _inherit = "sale.commission.make.settle"

    def _get_settlement(self, agent, company, sett_from, sett_to):
        if company.commission_settlement_company:
            company = company.commission_settlement_company
        return super(SaleCommissionMakeSettle, self)._get_settlement(
            agent, company, sett_from, sett_to
        )

    def _prepare_settlement_vals(self, agent, company, sett_from, sett_to):
        if company.commission_settlement_company:
            company = company.commission_settlement_company
        return super(SaleCommissionMakeSettle, self)._prepare_settlement_vals(
            agent, company, sett_from, sett_to
        )
