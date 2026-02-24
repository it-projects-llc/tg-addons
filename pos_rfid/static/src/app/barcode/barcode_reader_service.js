/** @odoo-module **/

import {BarcodeReader} from "@point_of_sale/app/barcode/barcode_reader_service";
import {patch} from "@web/core/utils/patch";
import {session} from "@web/session";
import {unhexForOdoo} from "../../js/unhex";

patch(BarcodeReader.prototype, {
    _scan(code) {
        return super._scan(unhexForOdoo(session, code));
    },
});
