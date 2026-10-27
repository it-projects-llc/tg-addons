from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    is_period = fields.Boolean(related="attribute_id.is_period")
    start_date = fields.Date(compute="_compute_start_date", store=True, readonly=False)
    end_date = fields.Date(compute="_compute_end_date", store=True, readonly=False)

    @api.depends(
        "attribute_id.is_period", "product_attribute_value_id.default_start_date"
    )
    def _compute_start_date(self):
        for record in self:
            if record.attribute_id.is_period and not record.start_date:
                record.start_date = record.product_attribute_value_id.default_start_date

    @api.depends(
        "attribute_id.is_period", "product_attribute_value_id.default_end_date"
    )
    def _compute_end_date(self):
        for record in self:
            if record.attribute_id.is_period and not record.end_date:
                record.end_date = record.product_attribute_value_id.default_end_date

    @api.constrains("start_date", "end_date")
    def _check_period(self):
        for ptav in self.filtered("is_period"):
            if not ptav.start_date:
                raise ValidationError(
                    _(
                        "Start date is not given",
                    )
                )
            elif not ptav.end_date:
                raise ValidationError(
                    _(
                        "End date is not given",
                    )
                )
            elif ptav.start_date > ptav.end_date:
                raise ValidationError(
                    _(
                        "Start date should not be greater than end date",
                    )
                )
