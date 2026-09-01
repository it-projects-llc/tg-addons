from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_shop_ref_id = fields.Many2one(
        related="pos_config_id.shop_ref_id", readonly=False
    )
    pos_auto_duplicate_invoices = fields.Boolean(
        related="pos_config_id.auto_duplicate_invoices", readonly=False
    )
    pos_show_auto_duplicate_invoices = fields.Boolean(
        related="pos_config_id.show_auto_duplicate_invoices", readonly=False
    )
    pos_show_return_products = fields.Boolean(
        related="pos_config_id.show_return_products", readonly=False
    )
    pos_show_invoice_button = fields.Boolean(
        related="pos_config_id.show_invoice_button", readonly=False
    )
    pos_debug_auto_duplicate_invoices = fields.Boolean(
        related="pos_config_id.debug_auto_duplicate_invoices", readonly=False
    )
    pos_customer_deselection_interval_readonly = fields.Boolean(
        compute="_compute_pos_customer_deselection_interval_readonly"
    )

    @api.depends("pos_auto_duplicate_invoices")
    def _compute_pos_customer_deselection_interval_readonly(self):
        for record in self:
            record.pos_customer_deselection_interval_readonly = (
                record.pos_auto_duplicate_invoices
            )

    @api.onchange("pos_auto_duplicate_invoices")
    def _onchange_pos_show_auto_duplicate_invoices(self):
        for record in self.filtered("pos_auto_duplicate_invoices"):
            record.pos_customer_deselection_interval = 0
