/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { SetPricelistButton } from "@point_of_sale/app/screens/product_screen/control_buttons/pricelist_button/pricelist_button";

patch(SetPricelistButton.prototype, {
    setup() {
        super.setup();
        this.isDisabled = !this.pos.user.hasGroupEnablePricelistButton;
    },

    async click() {
        if (this.isDisabled) return;
        await super.click();
    },
});
