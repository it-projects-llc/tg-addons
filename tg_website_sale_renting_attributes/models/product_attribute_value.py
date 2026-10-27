from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    default_start_date = fields.Date()
    default_end_date = fields.Date()

    @api.constrains("attribute_id.is_period", "default_start_date", "default_end_date")
    def _check_period_required_fields(self):
        for record in self:
            if not record.attribute_id.is_period:
                continue

            if not record.default_start_date:
                raise ValidationError(
                    _("Default start date should be set for period attribute")
                )

            if not record.default_end_date:
                raise ValidationError(
                    _("Default end date should be set for period attribute")
                )

            if record.default_start_date > record.default_end_date:
                raise ValidationError(
                    _(
                        "Default start date should not be greater than default end date",  # noqa: E501
                    )
                )
