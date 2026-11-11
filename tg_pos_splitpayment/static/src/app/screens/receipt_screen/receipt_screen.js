/** @odoo-module */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(ReceiptScreen.prototype, {
    async orderDone() {
        const splitGroupId = this.currentOrder.tgSplitGroupId;
        const nextOrder = splitGroupId ? this.pos.orders.find(o => o.tgSplitGroupId === splitGroupId && !o.finalized && o.uid !== this.currentOrder.uid) : null;
        
        if (nextOrder) {
            await this.env.services.popup.add(ErrorPopup, {
                title: _t("Cannot Create New Order"),
                body: _t("You cannot create a new order until all the split orders are paid."),
            });
            return;
        }
        super.orderDone(...arguments);
    },
    async resumeOrder() {
        const splitGroupId = this.currentOrder.tgSplitGroupId;
        const nextOrder = splitGroupId ? this.pos.orders.find(o => o.tgSplitGroupId === splitGroupId && !o.finalized && o.uid !== this.currentOrder.uid) : null;
        if (nextOrder) {
            this.pos.orders.forEach(o => {
                if (o.tgSplitGroupId === splitGroupId) {
                    o.isSplitGroupPaid = true;
                }
            });

            this.pos.removeOrder(this.currentOrder);
            this.pos.set_order(nextOrder);
            this.pos.resetProductScreenSearch();
            this.pos.showScreen("PaymentScreen");
            return;
        }
        return super.resumeOrder(...arguments);
    }
});
