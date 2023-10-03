from odoo.http import route, request
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController


class WebsiteEventSaleExtendController(WebsiteEventSaleController):
    @route()
    def registration_confirm(self, *args, **post):
        order = request.website.sale_get_order(force_create=False)
        if order:
            order.sudo().unlink()
        return super(WebsiteEventSaleExtendController, self).registration_confirm(*args, **post)
