/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useState } from "@odoo/owl";

export class SplitPaymentPopup extends AbstractAwaitablePopup {
    static template = "tg_pos_splitpayment.SplitPaymentPopup";
    static defaultProps = {
        title: _t("Split Payment"),
    };

    setup() {
        super.setup();
        this.pos = usePos();
        this.maxSplit = this.pos.config.pos_max_split_orders || 3;
        this.state = useState({
            splitParts: 3 > this.maxSplit ? this.maxSplit : 3,
            errorMessage: "",
        });
    }

    getPayload() {
        return this.state.splitParts;
    }

    confirm() {
        if (this.state.splitParts < 2) {
            this.state.errorMessage = _t("Minimum 2 orders required.");
            return;
        }
        if (this.state.splitParts > this.maxSplit) {
            this.state.errorMessage = _t(`Maximum allowed is ${this.maxSplit}.`);
            return;
        }
        this.state.errorMessage = "";
        super.confirm();
    }

    increment() {
        if (this.state.splitParts < this.maxSplit) {
            this.state.splitParts++;
        }
    }

    decrement() {
        if (this.state.splitParts > 2) {
            this.state.splitParts--;
        }
    }
}
