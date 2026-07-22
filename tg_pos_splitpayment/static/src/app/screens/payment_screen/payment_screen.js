/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async _finalizeValidation() {
        await super._finalizeValidation(...arguments);
        if (this.pos.tgNextSplitOrders && this.pos.tgNextSplitOrders.length > 0) {
            const nextOrderUid = this.pos.tgNextSplitOrders.shift();
            // get order from pos.orders
            const nextOrder = this.pos.orders.find(o => o.uid === nextOrderUid);
            if (nextOrder) {
                this.pos.set_order(nextOrder);
                this.pos.showScreen("ProductScreen");
            }
        }
    }
});
