# ruff: noqa: B023

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

    from odoo.addons.website_sale.models.sale_order import (  # pylint: disable=reimported
        SaleOrder,
        random,
    )

    def _cart_accessories(self):
        """ Suggest accessories based on 'Accessory Products' of products in cart """
        product_ids = set(self.website_order_line.product_id.ids)
        all_accessory_products = self.env['product.product']
        for line in self.website_order_line.filtered('product_id'):
            accessory_products = line.product_id.product_tmpl_id._get_website_accessory_product()
            accessory_products = accessory_products.filtered(lambda x, order=line.order_id: not x.rent_ok or order._can_rent_this_product(x))  # <--- added this
            if accessory_products:
                # Do not read ptavs if there is no accessory products to filter
                combination = line.product_id.product_template_attribute_value_ids + line.product_no_variant_attribute_value_ids
                all_accessory_products |= accessory_products.filtered(lambda product:
                    product.id not in product_ids
                    and product.filtered_domain(self.env['product.product']._check_company_domain(line.company_id))
                    and product._is_variant_possible(parent_combination=combination)
                    and (
                        not self.website_id.prevent_zero_price_sale
                        or product._get_contextual_price()
                    )
                )

        return random.sample(all_accessory_products, len(all_accessory_products))

    SaleOrder._cart_accessories = _cart_accessories

    from odoo.addons.website_sale_stock_renting.models.sale_order import (  # pylint: disable=reimported
        SaleOrder,
    )

    def _is_valid_renting_dates(self):
        """ Override to take into account the preparation time."""
        res = super(SaleOrder, self)._is_valid_renting_dates()
        rental_order_lines = self.order_line.filtered('reservation_begin')
        if not rental_order_lines or not res:
            return res
        max_padding_time = max(rental_order_lines.product_id.mapped('preparation_time'), default=0)
        initial_time = self.rental_start_date - timedelta(hours=max_padding_time)
        return initial_time >= fields.Datetime.now() - timedelta(days=1)   # <--- changes here

    SaleOrder._is_valid_renting_dates = _is_valid_renting_dates

    from odoo.addons.website_sale_renting.models.product_template import (
        UTC,
        UserError,
        _,
        api,
        relativedelta,
        request,
        timezone,
    )

    @api.model
    def _get_default_renting_dates(self, start_date, end_date, duration, unit):
        """ Get default renting dates to help user

        :param datetime start_date: a start_date which is directly returned if defined
        :param datetime end_date: a end_date which is directly returned if defined
        :param int duration: the duration expressed in int, in the unit given
        :param string unit: The duration unit, which can be 'hour', 'day', 'week' or 'month'
        """
        if start_date and end_date and start_date >= end_date:
            raise UserError(_("Please choose a return date that is after the pickup date."))

        if start_date or end_date:
            return start_date, end_date

        default_start_dt = self._get_default_start_date()
        if unit == 'hour':
            default_end_dt = self._get_default_end_date(default_start_dt, duration, unit)
        else:
            # <-- changes start
            # If unit in day, week, month, take into account the entire day.
            # 21st + 1 day --> from 21st 00:00:00 to 22nd 23:59:59
            # default_start_dt = datetime.combine(default_start_dt.date(), datetime.min.time())
            # yes, we did commented it out
            # <-- changes end
            # remove a second to avoid adding a day (from date point of view)
            default_end_dt = self._get_default_end_date(default_start_dt + relativedelta(seconds=-1), duration, unit)
            # Consider the timezone if frontend request
            # Return the UTC value according to the client
            # because the frontend will convert values according to its timezone
            # (and without conversion, we risk changing day).
            # <-- changes start
            # Use only Panama timezone
            if request and request.is_frontend:
                PANAMA_TZ = timezone("America/Panama")
                default_start_dt = PANAMA_TZ.localize(default_start_dt).astimezone(UTC)
                default_end_dt = PANAMA_TZ.localize(default_end_dt).astimezone(UTC)
            # <-- changes end
        return default_start_dt, default_end_dt
