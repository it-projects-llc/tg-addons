def post_load():
    from odoo.addons.sale_renting.models.sale_order_line import SaleOrderLine

    def _get_sale_order_line_multiline_description_sale(self):
        res = super(SaleOrderLine, self)._get_sale_order_line_multiline_description_sale()
        if self.is_rental:
            # <--- changes start
            if self.product_id.rent_via_period_ok:
                start_date, end_date = self._detect_start_end_date()
                self.order_id.write({
                    "rental_start_date": start_date,
                    "rental_return_date": end_date,
                })
            else:
                self.order_id._rental_set_dates()
            # <--- changes end
            res += self._get_rental_order_line_description()
        return res

    SaleOrderLine._get_sale_order_line_multiline_description_sale = _get_sale_order_line_multiline_description_sale
