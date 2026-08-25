/** @odoo-module */

import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {patch} from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    getNumpadButtons() {
        const r = super.getNumpadButtons();
        return r.map((button) => {
            if (button.value == "-" && !this.pos.user.hasGroupShowPMInProductScreen) {
                button.class += " disabled";
            }
            return button;
        });
    },
});
