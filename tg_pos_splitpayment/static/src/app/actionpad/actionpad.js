/** @odoo-module */

import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { patch } from "@web/core/utils/patch";
import { SplitPaymentPopup } from "../popups/split_payment_popup/split_payment_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(ActionpadWidget.prototype, {
    async onClickSplitPayment() {
        const order = this.pos.get_order();
        if (order.get_orderlines().length === 0) {
            this.env.services.popup.add(ErrorPopup, {
                title: "Empty Order",
                body: "There are no products in the order to split.",
            });
            return;
        }
        const { confirmed, payload: splitParts } = await this.env.services.popup.add(SplitPaymentPopup);
        if (confirmed) {
            this.pos.showScreen("SplitPaymentScreen", {
                order: order,
                splitParts: splitParts,
            });
        }
    }
});
