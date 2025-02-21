from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    shop_ref_id = fields.Many2one("pos.shop", string="Shop")
    auto_duplicate_invoices = fields.Boolean("Automatic invoice duplication")
    show_auto_duplicate_invoices = fields.Boolean(
        compute="_compute_show_auto_duplicate_invoices"
    )
    debug_auto_duplicate_invoices = fields.Boolean(
        "Debug automatic invoice duplication"
    )

    group_show_customer_button_id = fields.Many2one(
        comodel_name="res.groups",
        compute="_compute_groups_tg",
    )
    group_show_pm_in_payment_screen_id = fields.Many2one(
        comodel_name="res.groups",
        compute="_compute_groups_tg",
    )

    # make sure you don't conflict with pos_access_right
    def _compute_groups_tg(self):
        self.update(
            {
                "group_show_customer_button_id": self.env.ref(
                    "tg_pos.group_show_customer_button"
                ).id,
                "group_show_pm_in_payment_screen_id": self.env.ref(
                    "tg_pos.group_show_pm_in_payment_screen"
                ).id,
            }
        )

    @api.depends("company_id.fiscal_company")
    def _compute_show_auto_duplicate_invoices(self):
        for config in self:
            config.show_auto_duplicate_invoices = bool(config.company_id.fiscal_company)
