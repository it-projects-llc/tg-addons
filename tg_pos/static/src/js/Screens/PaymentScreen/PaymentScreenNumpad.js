odoo.define("tg_pos.PaymentScreenNumpad", function (require) {
    "use strict";

    const PaymentScreenNumpad = require("point_of_sale.PaymentScreenNumpad");
    const Registries = require("point_of_sale.Registries");

    const TGPaymentScreenNumpad = (PaymentScreenNumpad) =>
        class extends PaymentScreenNumpad {
            get hasMinusControlRights() {
                return this.env.pos.get_cashier().hasGroupShowPMInPaymentScreen;
            }
        };

    Registries.Component.extend(PaymentScreenNumpad, TGPaymentScreenNumpad);

    return TGPaymentScreenNumpad;
});
