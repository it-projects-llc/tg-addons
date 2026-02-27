/** @odoo-module **/

import "@website_sale_renting/js/website_sale_renting";
import {RentingMixinFix} from "@tg_website_sale_renting/js/renting_mixin";
import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include(RentingMixinFix);
