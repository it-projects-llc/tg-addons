from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    is_period = fields.Boolean()

    @api.constrains("is_period", "display_type")
    def _check_period_display_type(self):
        for record in self:
            if record.is_period and record.display_type not in ("radio", "select"):
                raise ValidationError(
                    _('Period attribute can have only "Radio" or "Select" display type')
                )
