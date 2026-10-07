from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_product_rentable = fields.Boolean(
        related=None, depends=[], compute="_compute_is_product_rentable", store=True
    )

    @api.depends("product_id")
    def _compute_is_product_rentable(self):
        for record in self:
            if record.product_id.rent_ok or record.product_id.rent_via_period_ok:
                record.is_product_rentable = True
            else:
                record.is_product_rentable = False

    def _get_rental_pricing_description(self):
        if self.product_id.rent_via_period_ok:
            return

        return super()._get_rental_pricing_description()
