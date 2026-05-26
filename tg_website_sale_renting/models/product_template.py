from pytz import UTC, timezone

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date

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
            return PANAMA_TZ.localize(res).astimezone(UTC).replace(tzinfo=None)
        else:
            return super()._get_default_start_date(*args, **kw)

    @api.model
    def _get_default_end_date(self, *args, **kw):
        company = self.company_id or self.env.company
        res = fields.Datetime.to_datetime(company.renting_default_end_date)

        if res:
            return PANAMA_TZ.localize(res).astimezone(UTC).replace(tzinfo=None)
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

    @api.constrains(
        "renting_min_start_date",
        "renting_max_end_date",
    )
    def _check_renting_dates_and_ranges1(self):
        def f(v):
            return format_date(self.env, v)

        for c in self:
            if (
                c.renting_min_start_date
                and c.renting_max_end_date
                and c.renting_min_start_date > c.renting_max_end_date
            ):
                raise ValidationError(
                    _(
                        "Renting minimal start date (%(min_start_date)s) cannot be greater than maximal end date (%(max_end_date)s)",  # noqa: E501
                        min_start_date=f(c.renting_min_start_date),
                        max_end_date=f(c.renting_max_end_date),
                    )
                )
