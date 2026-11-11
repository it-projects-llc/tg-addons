/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { SplitPaymentPopup } from "../popups/split_payment_popup/split_payment_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class SplitPaymentButton extends Component {
    static template = "tg_pos_splitpayment.SplitPaymentButton";

    setup() {
        this.pos = usePos();
    }
    _isDisabled() {
        const order = this.pos.get_order();
        return !order || order.get_orderlines().length === 0;
    }
    async click() {
        const order = this.pos.get_order();
        if (this._isDisabled()) {
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
}

ProductScreen.addControlButton({
    component: SplitPaymentButton,
    condition: function () {
        return true;
    },
});
