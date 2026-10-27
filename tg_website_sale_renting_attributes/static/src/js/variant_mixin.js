/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import {deserializeDateTime, formatDate} from "@web/core/l10n/dates";
import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";

import "@website_sale/js/website_sale";

const {DateTime} = luxon;

VariantMixin._onChangeCombinationPeriod = function (ev, $parent, combination) {
    const ctaWrapper = $parent[0].querySelector("#o_wsale_cta_wrapper");
    const el = document.querySelector("#not-allowed-to-rent-msg");

    if ($parent.find("#rentingDatesPeriod").data("deny-rent-this-product")) {
        el.innerHTML = _t(
            "This product cannot be mixed with other rental product(s) in the cart due to different rental periods availability setup. Please complete the order for the one added to cart first or remove the product(s) from the cart to proceed."
        );
        el.style.display = "block";
        ctaWrapper.classList.replace("d-flex", "d-none");
        return;
    }

    if (combination.start_date) {
        document.querySelector("input[name=renting_period_start_date]").value =
            formatDate(deserializeDateTime(combination.start_date));

        if (DateTime.now().endOf("day") > DateTime.fromSQL(combination.start_date)) {
            el.innerHTML = _t("Cannot rent from past date");
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
