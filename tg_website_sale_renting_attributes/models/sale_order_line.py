from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.tg_website_sale_renting.models.product_template import make_panana_dt


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

    def _detect_start_end_date(self):
        period_ptav = self.product_no_variant_attribute_value_ids.filtered("is_period")
        if not period_ptav:
            raise UserError(
                _(
                    "Period attribute is not set for product %s",
                    self.product_id.display_name,
                )
            )
        elif len(period_ptav) > 1:
            raise UserError(
                _(
                    "Too many period attributes for product %s",
                    self.product_id.display_name,
                )
            )

        start_date = period_ptav.start_date
        if not start_date:
            raise UserError(
                _("Period attribute %s does not have start date", period_ptav)
            )

        end_date = period_ptav.end_date
        if not end_date:
            raise UserError(
                _("Period attribute %s does not have end date", period_ptav)
            )

        return make_panana_dt(start_date), make_panana_dt(end_date)
