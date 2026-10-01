from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    is_period = fields.Boolean(related="attribute_id.is_period")

    start_date = fields.Date()
    end_date = fields.Date()

    @api.constrains("is_period", "start_date", "end_date")
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
