/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async _finalizeValidation() {
        // Mark the split group as paid
        const splitGroupId = this.currentOrder.tgSplitGroupId;
        if (splitGroupId) {
            this.pos.orders.forEach(o => {
                if (o.tgSplitGroupId === splitGroupId) {
                    o.isSplitGroupPaid = true;
                }
            });
        }
        await super._finalizeValidation(...arguments);
    }
});
