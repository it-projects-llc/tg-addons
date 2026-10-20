from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.tg_website_sale_renting.models.product_template import make_panana_dt


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rent_via_period_ok = fields.Boolean("Can be Rented via attributes")

    @api.onchange("rent_via_period_ok")
    def _onchange_rent_via_period_ok(self):
        if self.rent_via_period_ok:
            self.rent_ok = False

    @api.onchange("rent_ok")
    def _onchange_rent_ok(self):
        if self.rent_ok:
            self.rent_via_period_ok = False

    @api.constrains("rent_ok", "rent_via_period_ok")
    def _check_rent_oks(self):
        for record in self:
            if record.rent_ok and record.rent_via_period_ok:
                raise ValidationError(
                    _("Product cannot be rented with and without attributes")
                )

    def _check_rent_attributes(self):
        for record in self:
            period_attributes = record.attribute_line_ids.mapped(
                "attribute_id"
            ).filtered("is_period")
            if record.rent_via_period_ok and not period_attributes:
                raise ValidationError(
                    _(
                        "No period attributes given for product, "
                        "that is marked as can be rented via attributes"
                    )
                )
            elif not record.rent_via_period_ok and period_attributes:
                raise ValidationError(
                    _(
                        "Cannot use period attributes, "
                        "if product is not marked as can be rented via attributes"
                    )
                )

    def _get_product_price_context(self, combination):
        res = super()._get_product_price_context(combination)
        if self.rent_via_period_ok:
            period_ptav = combination.filtered("is_period")
            res.update(
                {
                    "start_date": period_ptav.start_date,
                    "end_date": period_ptav.end_date,
                }
            )
        return res

    def _get_additionnal_combination_info(
        self, product_or_template, quantity, date, website
    ):
        res = super()._get_additionnal_combination_info(
            product_or_template, quantity, date, website
        )

        if not product_or_template.rent_via_period_ok:
            return res

        res.update(
            is_rental_via_attributes=True,
            start_date=make_panana_dt(product_or_template.env.context["start_date"]),
            end_date=make_panana_dt(product_or_template.env.context["end_date"]),
        )

        return res

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._check_rent_attributes()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._check_rent_attributes()
        return res
