odoo.define("tg_pos.PaymentScreen", function (require) {
    "use strict";

    const { useBarcodeReader } = require('point_of_sale.custom_hooks');
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");

    const TGPaymentScreen = (x) => class extends x {
        constructor() {
            super(...arguments);
            useBarcodeReader({
                client: this._barcodeClientAction,
                error: this._barcodeErrorAction,
            });

        }
        _barcodeClientAction(code) {
            const partner = this.env.pos.db.get_partner_by_barcode(code.code);
            if (partner) {
                if (this.currentOrder.get_client() !== partner) {
                    this.currentOrder.set_client(partner);
                    this.currentOrder.updatePricelist(partner);
                }
                return true;
            }
            this._barcodeErrorAction(code);
            return false;
        }

        _barcodeErrorAction(code) {
            this.showPopup('ErrorBarcodePopup', { code: this._codeRepr(code) });
        }
    };

    Registries.Component.extend(PaymentScreen, TGPaymentScreen);

    return TGPaymentScreen;
});
