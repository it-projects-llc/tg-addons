/** @odoo-module **/
/* global Modal */

import {jsonrpc} from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SplitPaymentModal = publicWidget.Widget.extend({
    selector: "#split_payment_modal",
    events: {
        "submit form": "_onSubmit",
    },

    _getPost: function () {
        var post = {};
        this.$el.find("input,select").each(function () {
            const name = $(this).attr("name");
            const value = $(this).val();

            if (["payment_count"].includes(name)) {
                post[name] = parseInt(value, 10);
            } else if (["deposit"].includes(name)) {
                post[name] = parseFloat(value);
            } else {
                post[name] = value;
            }
        });
        return post;
    },

    _onSubmit(ev) {
        ev.preventDefault();
        const $form = $(ev.currentTarget).closest("form");
        const post = this._getPost();

        return jsonrpc($form.attr("action"), post).then(async function (modal) {
            var $modal = $(modal);
            $modal.appendTo(document.body);
            const modalBS = new Modal($modal[0], {backdrop: "static", keyboard: false});
            modalBS.show();
        });
    },
});
