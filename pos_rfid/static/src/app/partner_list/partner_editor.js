/** @odoo-module **/

import {PartnerDetailsEdit} from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
import {patch} from "@web/core/utils/patch";
import {unhexForOdoo} from "../../js/unhex";
import {session} from "@web/session";

patch(PartnerDetailsEdit.prototype, {
    onChangeField(fname, event) {
        if (fname === "Barcode") {
            this.changes.barcode = unhexForOdoo(session, event.target.value);
        }
    },
});
