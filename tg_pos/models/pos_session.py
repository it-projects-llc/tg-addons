from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _get_pos_ui_res_users(self, params):
        res = super()._get_pos_ui_res_users(params)
        user_id = res.get("id")
        if user_id:
            user = self.env["res.users"].browse(user_id)
            groups = user.groups_id
            config = self.config_id
            res.update(
                hasGroupShowCustomerButton=config.group_show_customer_button_id  # noqa: E501
                in groups,
                hasGroupShowPMInPaymentScreen=config.group_show_pm_in_payment_screen_id  # noqa: E501
                in groups,
                hasGroupEnablePricelistButton=config.group_enable_pricelist_button_id
                in groups,
            )
        return res
