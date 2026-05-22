from pytz import UTC, timezone

from odoo import api, fields, models

PANAMA_TZ = timezone("America/Panama")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    renting_min_start_date = fields.Date()
    renting_max_end_date = fields.Date()

    @api.model
    def _get_default_start_date(self, *args, **kw):
        company = self.company_id or self.env.company
        res = fields.Datetime.to_datetime(company.renting_default_start_date)
        if res:
            return PANAMA_TZ.localize(res).astimezone(UTC)
        else:
            return super()._get_default_start_date(*args, **kw)

    @api.model
    def _get_default_end_date(self, *args, **kw):
        company = self.company_id or self.env.company
        res = fields.Datetime.to_datetime(company.renting_default_end_date)

        if res:
            return PANAMA_TZ.localize(res).astimezone(UTC)
        else:
            return super()._get_default_end_date(*args, **kw)

    def _get_renting_min_start_date(self):
        company = self.company_id or self.env.company
        dates = list(
            filter(
                lambda x: x,
                self.mapped("renting_min_start_date")
                + [company.renting_min_start_date],
            )
        )
        if dates:
            res = max(dates)
        else:
            res = False
        return fields.Datetime.to_datetime(res)

    def _get_renting_max_end_date(self):
        company = self.company_id or self.env.company
        dates = list(
            filter(
                lambda x: x,
                self.mapped("renting_max_end_date") + [company.renting_max_end_date],
            )
        )
        if dates:
            res = min(dates)
        else:
            res = False
        return fields.Datetime.to_datetime(res)
