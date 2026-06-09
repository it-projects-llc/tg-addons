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

    from odoo.addons.website_sale_stock_renting.models.sale_order import (  # pylint: disable=reimported
        SaleOrder,
    )

    def _is_valid_renting_dates(self):
        """ Override to take into account the preparation time."""
        res = super()._is_valid_renting_dates()
        rental_order_lines = self.order_line.filtered('reservation_begin')
        if not rental_order_lines or not res:
            return res
        max_padding_time = max(rental_order_lines.product_id.mapped('preparation_time'), default=0)
        initial_time = self.rental_start_date - timedelta(hours=max_padding_time)
        return initial_time >= fields.Datetime.now() - timedelta(days=1)   # <--- changes here

    SaleOrder._is_valid_renting_dates = _is_valid_renting_dates
