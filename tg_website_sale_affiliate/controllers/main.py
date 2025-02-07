from odoo.http import request

from odoo.addons.website_sale_affiliate.controllers.main import WebsiteSale as Base


class WebsiteSale(Base):
    def _store_affiliate_info(self, **kwargs):
        affiliate_request = super()._store_affiliate_info(**kwargs)
        if affiliate_request:
            promo_code = affiliate_request.affiliate_id.promo_code
            if promo_code:
                request.session["pending_coupon_code"] = promo_code

        return affiliate_request
