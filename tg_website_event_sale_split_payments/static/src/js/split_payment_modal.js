/** @odoo-module **/
/* global Modal */

import {_t} from "@web/core/l10n/translation";
import dom from "@web/legacy/js/core/dom";
import {jsonrpc} from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SplitPaymentModal = publicWidget.Widget.extend({
    selector: "#split_payment_modal",
    events: {
        "blur input[name=deposit]": "_onBlurDeposit",
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

    start: function () {
        this._super.apply(this, arguments);
        this._onBlurDeposit();
    },

    _onBlurDeposit: async function () {
        this.$el.find(".additional-fee").html(_t("Calculating additional fee..."));
        const output = await jsonrpc(
            "/shop/cart/calculate_additional_fee_on_split_payments",
            this._getPost()
        );
        this.$el.find(".additional-fee").html(output);
    },

    _onSubmit: async function (ev) {
        ev.preventDefault();
        const $form = $(ev.currentTarget).closest("form");
        const post = this._getPost();

        const btnEl = ev.currentTarget.querySelector('button[type="submit"]');
        const removeLoadingEffect = dom.addButtonLoadingEffect(btnEl);

        try {
            const modal = await jsonrpc($form.attr("action"), post);
            const $modal = $(modal);
            $modal.appendTo(document.body);
            const modalBS = new Modal($modal[0], {backdrop: "static", keyboard: false});
            modalBS.show();
        } catch (e) {
            removeLoadingEffect();
            throw e;
        }

        setTimeout(() => {
            removeLoadingEffect();
        }, 1000);
    },
});
