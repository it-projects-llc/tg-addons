import json

from odoo import _
from odoo.exceptions import UserError
from odoo.http import request, route
from odoo.tools import format_amount

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleSplitPaymentController(WebsiteSale):
    @route()
    def shop_payment(self, **post):
        resp = super().shop_payment(**post)
        if resp.status_code != 200:
            return resp

        website_sale_order = resp.qcontext.get("website_sale_order")
        if not website_sale_order or website_sale_order._is_public_order():
            return resp

        amount_total = website_sale_order.amount_total
        min_deposit_abs = website_sale_order.company_id.invoice_plan_min_deposit_abs

        if amount_total < min_deposit_abs:
            return resp

        split_payment_periods = website_sale_order._get_allowed_split_payment_periods()
        if not split_payment_periods:
            return resp

        min_deposit_percent = (
            website_sale_order.company_id.invoice_plan_min_deposit_percent
        )
        max_deposit_percent = (
            website_sale_order.company_id.invoice_plan_max_deposit_percent
        )

        resp.qcontext.update(
            show_split_order=True,
            min_deposit=max(
                min_deposit_percent * amount_total / 100,
                min_deposit_abs,
            ),
            max_deposit=max_deposit_percent * amount_total / 100,
            max_installments_data=json.dumps(
                {k: v["max_installments"] for k, v in split_payment_periods.items()}
            ),
            split_payment_periods=split_payment_periods,
        )

        return resp

    @route(
        "/shop/cart/make_invoice_plan",
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def make_invoice_plan(self, deposit, payment_count, period):
        order = request.website.sale_get_order().sudo()
        if not order:
            raise UserError(_("No cart detected"))

        order._generate_invoice_plan_for_event(deposit, payment_count, period)

        return request.env["ir.ui.view"]._render_template(
            "tg_website_event_sale_split_payments.suggested_invoice_plan",
            {
                "order": order,
            },
        )

    @route(
        "/shop/cart/go_to_first_invoice_plan",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def shop_go_to_first_invoice_plan(self):
        order = request.website.sale_get_order()
        if not order:
            return request.redirect("/shop/cart")

        if not order.invoice_plan_ids[:1]:
            return request.redirect("/shop/payment")

        invoice = order._prepare_first_plan_payment()
        return request.redirect(invoice.get_portal_url())

    @route(
        "/shop/cart/calculate_additional_fee_on_split_payments",
        auth="public",
        type="json",
        website=True,
    )
    def shop_cart_calculate_additional_fee_on_split_payments(self, deposit, **kw):
        order = request.website.sale_get_order().sudo()
        if not order:
            raise UserError(_("No cart detected"))

        fee = order._calculate_additional_fee_for_splitting(deposit)
        if not fee:
            return _("No additional fee required")

        return _(
            "%s additional fee is applied if you use this payment method",
            format_amount(request.env, fee, order.currency_id),
        )
