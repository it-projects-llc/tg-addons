/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(Order.prototype, {
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (this.tgSplitGroupId) {
            json.tgSplitGroupId = this.tgSplitGroupId;
        }
        if (this.isSplitGroupPaid !== undefined) {
            json.isSplitGroupPaid = this.isSplitGroupPaid;
        }
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        if (json.tgSplitGroupId) {
            this.tgSplitGroupId = json.tgSplitGroupId;
        }
        if (json.isSplitGroupPaid !== undefined) {
            this.isSplitGroupPaid = json.isSplitGroupPaid;
        }
    }
});

patch(PosStore.prototype, {
    add_new_order() {
        if (this.orders.some(o => o.tgSplitGroupId && !o.finalized)) {
            this.env.services.popup.add(ErrorPopup, {
                title: _t("Cannot Create New Order"),
                body: _t("You cannot create a new order until all the split orders are paid."),
            });
            return null;
        }
        return super.add_new_order(...arguments);
    },
    showScreen(name, props) {
        const unpaidSplitOrder = this.orders.find(o => o.tgSplitGroupId && !o.finalized);
        if (name === "ProductScreen" && unpaidSplitOrder) {
            if (!this.get_order() || this.get_order().uid !== unpaidSplitOrder.uid) {
                this.set_order(unpaidSplitOrder);
            }
            return super.showScreen("PaymentScreen", props);
        }
        return super.showScreen(...arguments);
    },
    async closePos() {
        if (this.orders.some(o => o.tgSplitGroupId && !o.finalized)) {
            this.env.services.popup.add(ErrorPopup, {
                title: _t("Cannot Close Session"),
                body: _t("You cannot close a PoS session until all the split orders are paid."),
            });
            return;
        }
        return super.closePos(...arguments);
    }
});
