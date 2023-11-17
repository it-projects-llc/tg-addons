from odoo.http import request

from odoo.addons.website_sale_affiliate.controllers.main import WebsiteSale as Base


class WebsiteSale(Base):
    def _store_affiliate_info(self, **kwargs):
        super(WebsiteSale, self)._store_affiliate_info(**kwargs)
        aff_request_id = request.session.get("affiliate_request")
        if not aff_request_id:
            return

        aff_request = (
            request.env.user.sudo().env["sale.affiliate.request"].browse(aff_request_id)
        )
        affiliate = aff_request.affiliate_id
        if not affiliate.active:
            return

        if not affiliate.partner_id:
            return

        pricelist = affiliate.pricelist_id

        if not pricelist:
            return

        request.session["website_sale_current_pl"] = pricelist.id
