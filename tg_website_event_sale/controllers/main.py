from odoo.http import request, route

from odoo.addons.tg_website_sale_affiliate.controllers.main import WebsiteSale
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController


class WebsiteEventSaleExtendController(WebsiteEventSaleController):
    @route()
    def registration_confirm(self, *args, **post):
        order = request.website.sale_get_order(force_create=False)
        if order:
            SaleOrderLine = request.env["sale.order.line"].sudo()
            if (
                order.state == "draft"
                and "refund_source_line_id" in SaleOrderLine._fields
            ):
                refund_lines = SaleOrderLine.search(
                    [
                        ("order_id", "=", order.id),
                        ("display_type", "=", False),
                        ("refund_source_line_id", "!=", False),
                    ]
                )
                if not refund_lines:
                    order.sudo().unlink()
            elif order.state in ("draft", "cancel"):
                order.sudo().unlink()
        return super().registration_confirm(*args, **post)

    @route()
    def events(self, *args, **kw):
        override_event_list = False
        if kw.get("aff_ref"):
            tag_id = request.env.company.affilation_tag.id
            if tag_id:
                override_event_list = True
                kw["tags"] = f"[{tag_id}]"

        res = super().events(*args, **kw)
        sale = WebsiteSale()
        sale._store_affiliate_info(**kw)

        if override_event_list:
            res.qcontext["searches"]["tags"] = ""
            res.qcontext["search_tags"] = request.env["event.tag"]
            if len(res.qcontext["event_ids"]) == 1:
                event = res.qcontext["event_ids"]
                target_url = "/event/%s/register" % str(event.id)
                return request.redirect(target_url)

        return res

    @route()
    def event_page(self, *args, **kw):
        res = super().event_page(*args, **kw)
        sale = WebsiteSale()
        sale._store_affiliate_info(**kw)
        return res

    @route()
    def event(self, *args, **kw):
        res = super().event(*args, **kw)
        sale = WebsiteSale()
        sale._store_affiliate_info(**kw)
        return res

    @route()
    def event_register(self, *args, **kw):
        res = super().event_register(*args, **kw)
        sale = WebsiteSale()
        sale._store_affiliate_info(**kw)
        return res
