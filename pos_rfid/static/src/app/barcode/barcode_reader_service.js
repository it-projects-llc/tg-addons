/** @odoo-module **/

import {BarcodeReader} from "@point_of_sale/app/barcode/barcode_reader_service";
import {patch} from "@web/core/utils/patch";
import {session} from "@web/session";

patch(BarcodeReader.prototype, {
    _scan(code) {
        if (code && session.pos_hex_barcode) {
            let unhexed_code = parseInt(code, 16).toString();
            if (unhexed_code.length % 2) {
                unhexed_code = "0" + unhexed_code;
            }
            return super._scan(unhexed_code);
        }
        return super._scan(code);
    },
});
