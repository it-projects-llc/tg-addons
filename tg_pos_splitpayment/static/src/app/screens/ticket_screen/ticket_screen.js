/** @odoo-module */

import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(TicketScreen.prototype, {
    shouldHideDeleteButton(order) {
        if (order.tgSplitGroupId && !order.finalized) {
            return true;
        }
        return super.shouldHideDeleteButton(...arguments);
    },
    onCreateNewOrder() {
        if (this.pos.orders.some(o => o.tgSplitGroupId && !o.finalized)) {
            this.env.services.popup.add(ErrorPopup, {
                title: _t("Cannot Create New Order"),
                body: _t("You cannot create a new order until all the split orders are paid."),
            });
            return;
        }
        return super.onCreateNewOrder(...arguments);
    },
    async onDeleteOrder(order) {
        const splitGroupId = order.tgSplitGroupId;
        if (splitGroupId) {
            const relatedOrders = this.pos.orders.filter(o => o.tgSplitGroupId === splitGroupId && o.uid !== order.uid);
            for (const relOrder of relatedOrders) {
                this.pos.removeOrder(relOrder);
            }
        }
        return super.onDeleteOrder(order);
    }
});
