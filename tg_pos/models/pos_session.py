from odoo import _, models
from odoo.exceptions import UserError


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

        if not self:
            raise UserError(_("No sessions detected"))

        not_closed = self.filtered(lambda x: x.state != "closed")
        if not_closed:
            raise UserError(
                _(
                    "Following sessions are not closed: %s",
                    ", ".join(not_closed.mapped("display_name")),
                )
            )

        all_orders = self.mapped("order_ids")
        if not all_orders:
            raise UserError(_("No orders detected"))

        orders_without_invoices = all_orders.filtered(lambda x: not x.account_move)

        if not orders_without_invoices:
            raise UserError(_("No orders without invoices detected"))

        for _partner, orders in (
            orders_without_invoices.sorted("partner_id").grouped("partner_id").items()
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
                company_orders.write(
                    {
                        "account_move": new_move,
                        "state": "invoiced",
                    }
                )
                moves += new_move

        if not moves:
            raise UserError(_("No invoices generated"))

        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_out_invoice_type"
        )
        if len(moves) > 1:
            action["domain"] = [("id", "in", moves.ids)]
        else:
            form_view = [(self.env.ref("account.view_move_form").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = moves.id

        return action
