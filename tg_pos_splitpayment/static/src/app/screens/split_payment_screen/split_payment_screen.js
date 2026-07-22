/** @odoo-module */

import { registry } from "@web/core/registry";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, useState } from "@odoo/owl";
import { Numpad } from "@point_of_sale/app/generic_components/numpad/numpad";

export class SplitPaymentScreen extends Component {
    static template = "tg_pos_splitpayment.SplitPaymentScreen";
    static components = { Numpad };

    setup() {
        super.setup();
        this.pos = usePos();
        this.originalOrder = this.props.order;
        this.totalAmount = this.originalOrder.get_total_with_tax();
        
        const splitParts = this.props.splitParts || 3;
        const splits = [];
        for (let i = 0; i < splitParts; i++) {
            splits.push({
                id: i,
                name: `Order ${i + 1}`,
                amount: 0,
                isFirst: i === 0,
                amountStr: "0",
            });
        }
        splits[0].amount = this.totalAmount;
        splits[0].amountStr = this.env.utils.formatCurrency(this.totalAmount);

        this.state = useState({
            splits: splits,
            selectedId: 1, // default to select second order
        });
    }

    get selectedSplit() {
        return this.state.splits.find(s => s.id === this.state.selectedId);
    }

    selectSplit(id) {
        if (id !== 0) {
            this.state.selectedId = id;
        }
    }

    updateAmount(val) {
        const split = this.selectedSplit;
        if (!split || split.isFirst) return;

        if (val === "Backspace") {
            split.amountStr = split.amountStr.slice(0, -1);
            if (split.amountStr === "") split.amountStr = "0";
        } else if (val === "-") {
            if (split.amountStr.startsWith("-")) {
                split.amountStr = split.amountStr.substring(1);
            } else {
                split.amountStr = "-" + split.amountStr;
            }
        } else if (val === "." || val === ",") {
            if (!split.amountStr.includes(".")) {
                split.amountStr += ".";
            }
        } else {
            if (split.amountStr === "0") {
                split.amountStr = val;
            } else {
                split.amountStr += val;
            }
        }

        split.amount = parseFloat(split.amountStr) || 0;
        this._recalculateFirstOrder();
    }

    _recalculateFirstOrder() {
        let otherTotal = 0;
        for (let i = 1; i < this.state.splits.length; i++) {
            otherTotal += this.state.splits[i].amount;
        }
        this.state.splits[0].amount = this.totalAmount - otherTotal;
    }

    async confirm() {
        // Enforce proportional split
        const originalLines = this.originalOrder.get_orderlines();
        const splitsToCreate = this.state.splits.filter(s => s.amount !== 0);
        
        if (splitsToCreate.length === 0) {
            this.pos.showScreen("ProductScreen");
            return;
        }

        const newOrders = [];
        
        for (let i = 0; i < splitsToCreate.length; i++) {
            const split = splitsToCreate[i];
            const ratio = split.amount / this.totalAmount;
            
            let order;
            if (i === 0) {
                // modify original order
                order = this.originalOrder;
            } else {
                // Create new order
                order = this.pos.add_new_order();
            }
            newOrders.push(order);
        }

        // Apply quantities
        for (let j = 0; j < originalLines.length; j++) {
            const line = originalLines[j];
            const originalQty = line.get_quantity();
            
            for (let i = 0; i < splitsToCreate.length; i++) {
                const split = splitsToCreate[i];
                const ratio = split.amount / this.totalAmount;
                const newQty = originalQty * ratio;
                
                if (i === 0) {
                    // Update original line
                    line.set_quantity(newQty);
                } else {
                    // Add line to new order by cloning
                    const newLine = line.clone();
                    newLine.order = newOrders[i];
                    newLine.set_quantity(newQty);
                    newOrders[i].add_orderline(newLine);
                }
            }
        }

        // Set next orders to show
        if (newOrders.length > 1) {
            this.pos.tgNextSplitOrders = newOrders.slice(1).map(o => o.uid);
        }

        this.pos.set_order(newOrders[0]);
        this.pos.showScreen("ProductScreen");
    }

    back() {
        this.pos.showScreen("ProductScreen");
    }
}

registry.category("pos_screens").add("SplitPaymentScreen", SplitPaymentScreen);
