/** @odoo-module */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(Navbar.prototype, {
    async closeSession() {
        if (this.pos.orders.some(o => o.tgSplitGroupId && !o.finalized)) {
            await this.popup.add(ErrorPopup, {
                title: _t("Cannot Close Session"),
                body: _t("You cannot close a PoS session until all the split orders are paid."),
            });
            return;
        }
        return super.closeSession(...arguments);
    }
});
