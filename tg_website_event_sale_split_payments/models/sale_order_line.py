from datetime import timedelta

from odoo import models
from odoo.fields import Date

from ..const import DEFAULT_MAX_INSTALLMENT_DATE


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_price_total_using_max_tier_price(self):
        self.ensure_one()
        if self.event_ticket_id.max_tier_price:
            return self.product_uom_qty * self.event_ticket_id.max_tier_price
        else:
            return self.price_total

    def _get_max_installment_date(self):
        self.ensure_one()
        if self.display_type:
            return DEFAULT_MAX_INSTALLMENT_DATE

        security_days = timedelta(days=self.company_id.invoice_plan_security_days)

        # we use gettattr here, since I don't want
        # to put enterprise dependency to this module
        is_rental = getattr(self, "is_rental", False)
        if is_rental:
            return Date.to_date(self.start_date) - security_days

        company_max_installment_date = self.company_id.invoice_plan_max_installment_date

        if self.event_id:
            return min(self.event_id.max_installment_date, company_max_installment_date)

        return company_max_installment_date
