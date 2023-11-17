from odoo.http import route, request
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController
from odoo.addons.website_sale_affiliate.controllers.main import WebsiteSale


class WebsiteEventSaleExtendController(WebsiteEventSaleController):
    _store_affiliate_info = WebsiteSale._store_affiliate_info

    @route()
    def registration_confirm(self, *args, **post):
        order = request.website.sale_get_order(force_create=False)
        if order:
            order.sudo().unlink()
        return super(WebsiteEventSaleExtendController, self).registration_confirm(*args, **post)

    @route()
    def events(self, *args, **kw):
        res = super(WebsiteEventSaleExtendController, self).events(*args, **kw)
        self._store_affiliate_info(**kw)
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
