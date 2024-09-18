from odoo.http import request, route

from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController
from odoo.addons.website_sale_affiliate.controllers.main import WebsiteSale


class WebsiteEventSaleExtendController(WebsiteEventSaleController):
    _store_affiliate_info = WebsiteSale._store_affiliate_info

    @route()
    def registration_confirm(self, *args, **post):
        order = request.website.sale_get_order(force_create=False)
        if order and order.state in ("draft", "cancel"):
            order.sudo().unlink()
        return super(WebsiteEventSaleExtendController, self).registration_confirm(
            *args, **post
        )

    @route()
    def events(self, *args, **kw):
        override_event_list = False
        if kw.get("aff_ref"):
            tag_id = request.env.company.affilation_tag.id
            if tag_id:
                override_event_list = True
                kw["tags"] = f"[{tag_id}]"

        res = super(WebsiteEventSaleExtendController, self).events(*args, **kw)
        self._store_affiliate_info(**kw)

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
        res = super(WebsiteEventSaleExtendController, self).event_page(*args, **kw)
        self._store_affiliate_info(**kw)
        return res

    @route()
    def event(self, *args, **kw):
        res = super(WebsiteEventSaleExtendController, self).event(*args, **kw)
        self._store_affiliate_info(**kw)
        return res

    @route()
    def event_register(self, *args, **kw):
        res = super(WebsiteEventSaleExtendController, self).event_register(*args, **kw)
        self._store_affiliate_info(**kw)
        return res
