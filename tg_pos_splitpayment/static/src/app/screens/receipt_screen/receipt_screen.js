/** @odoo-module */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";

patch(ReceiptScreen.prototype, {
    orderDone() {
        if (this.pos.tgNextSplitOrders && this.pos.tgNextSplitOrders.length > 0) {
            const nextOrderUid = this.pos.tgNextSplitOrders.shift();
            const nextOrder = this.pos.orders.find(o => o.uid === nextOrderUid);
            if (nextOrder) {
                this.pos.removeOrder(this.currentOrder);
                this.pos.set_order(nextOrder);
                this.pos.resetProductScreenSearch();
                this.pos.showScreen("ProductScreen");
                return;
            }
        }
        super.orderDone(...arguments);
    }
});
