from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    renting_default_start_date = fields.Date(
        related="company_id.renting_default_start_date", readonly=False
    )

    renting_default_end_date = fields.Date(
        related="company_id.renting_default_end_date", readonly=False
    )

    renting_min_start_date = fields.Date(
        related="company_id.renting_min_start_date", readonly=False
    )

    renting_max_end_date = fields.Date(
        related="company_id.renting_max_end_date", readonly=False
    )

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

    @api.constrains(
        "renting_default_start_date",
        "renting_default_end_date",
    )
    def _check_renting_dates_and_ranges2(self):
        def f(v):
            return format_date(self.env, v)

        for c in self:
            if (
                c.renting_default_start_date
                and c.renting_default_end_date
                and c.renting_default_start_date > c.renting_default_end_date
            ):
                raise ValidationError(
                    _(
                        "Default renting start date (%(default_start_date)s) cannot be greater default renting end date (%(default_end_date)s)",  # noqa: E501
                        default_start_date=f(c.renting_default_start_date),
                        default_end_date=f(c.renting_default_end_date),
                    )
                )

    @api.constrains(
        "renting_default_start_date",
        "renting_min_start_date",
    )
    def _check_renting_dates_and_ranges3(self):
        def f(v):
            return format_date(self.env, v)

        for c in self:
            if (
                c.renting_min_start_date
                and c.renting_default_start_date
                and c.renting_default_start_date < c.renting_min_start_date
            ):
                raise ValidationError(
                    _(
                        "Renting default start date (%(default_start_date)s) cannot be less than minimal start date (%(min_start_date)s)",  # noqa: E501
                        default_start_date=f(c.renting_default_start_date),
                        min_start_date=f(c.renting_min_start_date),
                    )
                )

    @api.constrains(
        "renting_default_end_date",
        "renting_max_end_date",
    )
    def _check_renting_dates_and_ranges4(self):
        def f(v):
            return format_date(self.env, v)

        for c in self:
            if (
                c.renting_max_end_date
                and c.renting_default_end_date
                and c.renting_default_end_date > c.renting_max_end_date
            ):
                raise ValidationError(
                    _(
                        "Renting default end date (%(default_end_date)s) cannot be greater than maximal end date (%(max_end_date)s)",  # noqa: E501
                        default_end_date=f(c.renting_default_end_date),
                        max_end_date=f(c.renting_max_end_date),
                    )
                )
