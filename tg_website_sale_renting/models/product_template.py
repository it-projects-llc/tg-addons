from pytz import UTC, timezone

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date

PANAMA_TZ = timezone("America/Panama")


def make_panana_dt(x):
    if not x:
        return x
    res = fields.Datetime.to_datetime(x)
    return PANAMA_TZ.localize(res).astimezone(UTC).replace(tzinfo=None)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    renting_min_start_date = fields.Date()
    renting_max_end_date = fields.Date()

    @api.model
    def _get_default_start_date(self, *args, **kw):
        if self.renting_min_start_date:
            res = self.renting_min_start_date
        else:
            company = self.company_id or self.env.company
            res = company.renting_default_start_date

        if res:
            return make_panana_dt(res)
        else:
            return super()._get_default_start_date(*args, **kw)

    @api.model
    def _get_default_end_date(self, *args, **kw):
        if self.renting_max_end_date:
            res = self.renting_max_end_date
        else:
            company = self.company_id or self.env.company
            res = company.renting_default_end_date

        if res:
            return make_panana_dt(res)
        else:
            return super()._get_default_end_date(*args, **kw)

    def _get_renting_min_start_date(self):
        self.ensure_one()
        company = self.company_id or self.env.company
        res = self.renting_min_start_date or company.renting_min_start_date
        return make_panana_dt(res)

    def _get_renting_max_end_date(self):
        self.ensure_one()
        company = self.company_id or self.env.company
        res = self.renting_max_end_date or company.renting_max_end_date
        return make_panana_dt(res)

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

    def _get_allowed_renting_periods(self, company):
        min_start_date = company.renting_min_start_date
        max_end_date = company.renting_max_end_date
        if self:
            return self.mapped(
                lambda x: (
                    make_panana_dt(x.renting_min_start_date or min_start_date),
                    make_panana_dt(x.renting_max_end_date or max_end_date),
                )
            )
        else:
            return [(make_panana_dt(min_start_date), make_panana_dt(max_end_date))]

    def _get_combination_info(
        self,
        combination=False,
        product_id=False,
        add_qty=1.0,
        parent_combination=False,
        only_template=False,
    ):
        self.ensure_one()

        combination = combination or self.env["product.template.attribute.value"]
        parent_combination = (
            parent_combination or self.env["product.template.attribute.value"]
        )

        if not product_id and not combination and not only_template:
            combination = self._get_first_possible_combination(parent_combination)

        res = super()._get_combination_info(
            combination, product_id, add_qty, parent_combination, only_template
        )

        period_ptav = combination.filtered("is_period")
        if period_ptav:
            res.update(
                start_date=make_panana_dt(period_ptav.start_date),
                end_date=make_panana_dt(period_ptav.end_date),
            )
        return res
