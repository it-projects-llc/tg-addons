def post_load():
    from odoo.addons.website_sale_renting.models.sale_order import (
        SaleOrder,
        fields,
        timedelta,
    )

    def _is_valid_renting_dates(self):
        """ Check if the pickup and return dates are valid.

        :return: Whether the pickup and return dates are valid.
        :rtype: bool
        """
        self.ensure_one()
        if not self.has_rented_products:
            return True
        if not (self.rental_start_date and self.rental_return_date):
            return False
        days_forbidden = self.company_id._get_renting_forbidden_days()
        # renting dates are in UTC, we need to convert them to the client's timezone
        # to check the day of the week correctly or we might get a day off
        start_dt, return_dt = self._get_localized_renting_dates()

        return (
            self.rental_start_date >= fields.Datetime.now() - timedelta(days=1)  # <--- changes here
            and start_dt.isoweekday() not in days_forbidden
            and return_dt.isoweekday() not in days_forbidden
            and self._get_renting_duration() >= self.company_id.renting_minimal_time_duration
        )

    SaleOrder._is_valid_renting_dates = _is_valid_renting_dates
