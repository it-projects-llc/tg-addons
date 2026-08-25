from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError

from .account_move import sentinel


def merge_line_values(invoice_lines):
    res = []
    product_line_indices = defaultdict(list)
    for t in invoice_lines:
        if t[0] != 0:
            raise NotImplementedError()

        line = t[2]
        if line.get("display_type"):
            continue

        if int(line.get("discount")) == 100:
            continue

        if not line.get("quantity"):
            continue

        product_id = line["product_id"]
        current_line_clean = line.copy()
        current_line_clean.pop("quantity")

        add_to_res = True
        for existing_product_line_index in product_line_indices[product_id]:
            product_line = res[existing_product_line_index][2]
            product_line_clean = product_line.copy()
            product_line_clean.pop("quantity")
            if product_line_clean == current_line_clean:
                product_line["quantity"] += line["quantity"]
                add_to_res = False
                break

        if add_to_res:
            new_product_line_index = len(res)
            product_line_indices[product_id].append(new_product_line_index)
            res.append((0, 0, line.copy()))

    return list(filter(lambda x: abs(x[2]["quantity"]) > 0.01, res))


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
                hasGroupShowPMInProductScreen=config.group_show_pm_in_product_screen_id  # noqa: E501
                in groups,
                hasGroupEnablePricelistButton=config.group_enable_pricelist_button_id
                in groups,
            )
        return res

    def _generate_grouped_pos_invoice(
        self, group_invoice_date=None, group_due_date=None
    ):
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

        for partner, orders in (
            orders_without_invoices.sorted("partner_id").grouped("partner_id").items()
        ):
            if not partner:
                continue

            for company, company_orders in (
                orders.sorted("company_id").grouped("company_id").items()
            ):
                # amount_total desc sorting is required to make sure,
                # that result move will be invoice, not refund
                # at least when there is at least one order with positive amount_total
                company_orders = company_orders.with_context(
                    sign_only_positive=sentinel
                ).sorted("amount_total", reverse=True)

                move_vals = company_orders[:1]._prepare_invoice_vals()

                for order in company_orders[1:]:
                    move_vals["invoice_line_ids"] += order._prepare_invoice_lines()

                move_vals["pos_sessions_origin"] = "\n".join(
                    [company.name] + company_orders.mapped("session_id.name")
                )
                move_vals["invoice_user_id"] = self.env.user.id
                if group_invoice_date:
                    move_vals["invoice_date"] = group_invoice_date

                if group_due_date:
                    move_vals["invoice_date_due"] = group_due_date

                move_vals.pop("ref", 0)
                move_vals.pop("invoice_origin", 0)
                move_vals.pop("partner_bank_id", 0)

                move_vals["invoice_line_ids"] = merge_line_values(
                    move_vals["invoice_line_ids"]
                )

                if not move_vals["invoice_line_ids"]:
                    continue

                new_move = (
                    company_orders[:1]
                    .with_context(no_message_post=sentinel)
                    ._create_invoice(move_vals)
                )
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
