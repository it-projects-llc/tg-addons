from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_plan_min_deposit_percent = fields.Float(
        string="Minimum advance payment (%)",
        config_parameter="tg_website_event_sale_split_payments.invoice_plan_min_deposit_percent",
    )
    invoice_plan_max_deposit_percent = fields.Float(
        string="Maximum advance payment (%)",
        config_parameter="tg_website_event_sale_split_payments.invoice_plan_max_deposit_percent",
    )

    @api.constrains(
        "invoice_plan_min_deposit_percent", "invoice_plan_max_deposit_percent"
    )
    def _check_invoice_plan_deposits(self):
        for settings in self:
            if (
                settings.invoice_plan_min_deposit_percent
                >= settings.invoice_plan_max_deposit_percent
            ):
                raise ValidationError(
                    _("Minimum advance payment should be less than maximum")
                )
