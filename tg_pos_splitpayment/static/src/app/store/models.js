/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.tgSplitGroupId = this.tgSplitGroupId || null;
        this.isSplitGroupPaid = this.isSplitGroupPaid || false;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.tgSplitGroupId = this.tgSplitGroupId;
        json.isSplitGroupPaid = this.isSplitGroupPaid;
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.tgSplitGroupId = json.tgSplitGroupId;
        this.isSplitGroupPaid = json.isSplitGroupPaid;
    }
});
