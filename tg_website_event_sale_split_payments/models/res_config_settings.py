from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import format_date


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_plan_min_deposit_percent = fields.Float(
        string="Minimum advance payment (%)",
        config_parameter="tg_website_event_sale_split_payments.invoice_plan_min_deposit_percent",
        help="Minimum percentage of the total payment to be paid as an advance",
    )
    invoice_plan_max_deposit_percent = fields.Float(
        string="Maximum advance payment (%)",
        config_parameter="tg_website_event_sale_split_payments.invoice_plan_max_deposit_percent",
        help="Maximum percentage of the total payment to be paid as an advance",
    )
    invoice_plan_min_deposit_abs = fields.Float(
        string="Minimum advance payment (absolute)",
        config_parameter="tg_website_event_sale_split_payments.invoice_plan_min_deposit_abs",
        help="""Minimum absolute value of total payment to be paid as an advance.
Also shopping carts below this
value won’t show the “split payment” option at checkout.""",
    )
    invoice_plan_last_installment_date = fields.Datetime(
        config_parameter="tg_website_event_sale_split_payments.last_installment_date",
        string="Last installment date",
        help="""The latest date that a split payment invoice can be created
(max allowed date for installments, except rental and shuttle products)
        """,
    )
    invoice_plan_security_days = fields.Integer(
        config_parameter="tg_website_event_sale_split_payments.invoice_plan_security_days",
        string="If set, it deducts days from last installment date",
    )
    invoice_plan_last_installment_description = fields.Char(
        compute="_compute_invoice_plan_last_installment_description"
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

    @api.depends("invoice_plan_last_installment_date", "invoice_plan_security_days")
    def _compute_invoice_plan_last_installment_description(self):
        for settings in self:
            if not settings.invoice_plan_last_installment_date:
                settings.invoice_plan_last_installment_description = ""
                continue

            last_installment_date = fields.Date.to_date(
                settings.invoice_plan_last_installment_date
                - timedelta(days=settings.invoice_plan_security_days)
            )

            settings.invoice_plan_last_installment_description = _(
                "Customers won't have installments after %s",
                format_date(self.env, last_installment_date),
            )
