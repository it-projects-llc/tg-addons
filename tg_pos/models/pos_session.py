from odoo import _, models


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

    def _generate_grouped_pos_invoice(self):
        moves = self.env["account.move"]

        for _partner, orders in (
            self.mapped("order_ids").sorted("partner_id").grouped("partner_id").items()
        ):
            for company, company_orders in (
                orders.sorted("company_id").grouped("company_id").items()
            ):
                move_vals = company_orders[:1]._prepare_invoice_vals()

                for order in company_orders[1:]:
                    move_vals["invoice_line_ids"] += order._prepare_invoice_lines()

                move_vals["narration"] = "\n".join(
                    [company.name] + company_orders.mapped("name")
                )
                move_vals["invoice_user_id"] = self.env.user.id
                move_vals.pop("ref", 0)
                move_vals.pop("invoice_origin", 0)

                new_move = company_orders[:1]._create_invoice(move_vals)
                moves += new_move

        return {
            "name": _("Customer Invoice"),
            "view_mode": "form",
            "view_id": self.env.ref("account.view_move_form").id,
            "res_model": "account.move",
            "context": "{'move_type':'out_invoice'}",
            "type": "ir.actions.act_window",
            "target": "current",
            "res_id": moves and moves.ids[0] or False,
        }
