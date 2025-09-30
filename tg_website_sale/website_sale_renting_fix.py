from odoo.http import request, route

from odoo.addons.website_sale_renting.controllers.variant import (
    WebsiteSaleRentingVariantController,
)
from odoo.addons.website_sale_renting_product_configurator.controllers.configurator import (  # noqa: E501
    RentingConfiguratorController,
)


class FixedRentingConfigurator(RentingConfiguratorController):
    @route()
    def show_advanced_configurator(self, *args, **kw):
        if (kw.get("context") or {}).get("start_date"):
            request.update_context(start_date=kw["context"]["start_date"])

        if (kw.get("context") or {}).get("end_date"):
            request.update_context(end_date=kw["context"]["end_date"])

        return super().show_advanced_configurator(*args, **kw)


class FixedWebsiteSaleRentingVariantController(WebsiteSaleRentingVariantController):
    @route()
    def get_combination_info_website(self, *args, **kw):
        if (kw.get("context") or {}).get("start_date"):
            kw["start_date"] = kw["context"]["start_date"]

        if (kw.get("context") or {}).get("end_date"):
            kw["end_date"] = kw["context"]["end_date"]

        return super().get_combination_info_website(*args, **kw)
