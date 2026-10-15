/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";
import {deserializeDateTime, formatDate} from "@web/core/l10n/dates";

import "@website_sale/js/website_sale";

const {DateTime} = luxon;

VariantMixin._onChangeCombinationPeriod = function (ev, $parent, combination) {
    if (combination.start_date) {
        document.querySelector("input[name=renting_period_start_date]").value =
            formatDate(deserializeDateTime(combination.start_date));

        const el = document.querySelector("#not-allowed-to-rent-msg");
        const ctaWrapper = $parent[0].querySelector("#o_wsale_cta_wrapper");
        if (DateTime.now().endOf("day") > DateTime.fromSQL(combination.start_date)) {
            el.innerHTML = "Cannot rent from past date";
            el.style.display = "block";
            ctaWrapper.classList.replace("d-flex", "d-none");
        } else {
            el.innerHTML = "";
            el.style.display = "none";
            ctaWrapper.classList.replace("d-none", "d-flex");
        }
    }

    if (combination.end_date) {
        document.querySelector("input[name=renting_period_end_date]").value =
            formatDate(deserializeDateTime(combination.end_date));
    }
};

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination: function () {
        this._super.apply(this, arguments);
        VariantMixin._onChangeCombinationPeriod.apply(this, arguments);
    },
});
