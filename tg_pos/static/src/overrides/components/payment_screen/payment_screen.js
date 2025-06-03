/** @odoo-module */

import {ErrorBarcodePopup} from "@point_of_sale/app/barcode/error_popup/barcode_error_popup";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {patch} from "@web/core/utils/patch";
import {useBarcodeReader} from "@point_of_sale/app/barcode/barcode_reader_hook";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();

        useBarcodeReader({
            client: this._barcodePartnerAction,
        });
    },

    async _barcodePartnerAction(code) {
        const partner = await this._getPartnerByBarcode(code);
        if (partner) {
            if (this.currentOrder.get_partner() !== partner) {
                this.currentOrder.set_partner(partner);
            }
            return null;
        }
        return this.popup.add(ErrorBarcodePopup, {code: code.base_code});
    },

    async _getPartnerByBarcode(code) {
        let partner = this.pos.db.get_partner_by_barcode(code.code);
        if (!partner) {
            // Find the partner in the backend by the barcode
            const foundPartnerIds = await this.orm.search("res.partner", [
                ["barcode", "=", code.code],
            ]);
            if (foundPartnerIds.length) {
                await this.pos._loadPartners(foundPartnerIds);
                // Assume that the result is unique.
                partner = this.pos.db.get_partner_by_id(foundPartnerIds[0]);
            }
        }
        return partner;
    },

    getNumpadButtons() {
        const res = super.getNumpadButtons();
        res.forEach((btn) => {
            if (btn.value === "-") {
                // TODO: этот метод есть?
                // TODO: css-ка с disabled нужна?
                btn.disabled = !this.pos.user.hasGroupShowPMInPaymentScreen;
            }
        });
        return res;
    },

    shouldDownloadInvoice() {
        if (this.pos.config.auto_duplicate_invoices) return false;
        return super.shouldDownloadInvoice();
    },
});
