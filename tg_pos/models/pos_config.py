from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    group_show_customer_button_id = fields.Many2one(
        comodel_name="res.groups",
        compute="_compute_groups_tg",  # make sure you don't conflict with pos_access_right
    )
    group_show_pm_in_payment_screen_id = fields.Many2one(
        comodel_name="res.groups",
        compute="_compute_groups_tg",
    )

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
