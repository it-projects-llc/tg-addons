/** @odoo-module **/

import {NFCButton} from "@pos_rfid/app/nfc_button/nfc_button";
import {Navbar} from "@point_of_sale/app/navbar/navbar";
import {patch} from "@web/core/utils/patch";

patch(Navbar, {
    components: {...Navbar.components, NFCButton},
});
