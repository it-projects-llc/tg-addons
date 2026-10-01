/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";
import {deserializeDateTime, formatDate} from "@web/core/l10n/dates";

import "@website_sale/js/website_sale";

VariantMixin._onChangeCombinationPeriod = function (ev, $parent, combination) {
    if (combination.start_date) {
        document.querySelector("input[name=renting_start_date]").value = formatDate(
            deserializeDateTime(combination.start_date)
        );
    }

    if (combination.end_date) {
        document.querySelector("input[name=renting_end_date]").value = formatDate(
            deserializeDateTime(combination.end_date)
        );
    }

    // TODO: не ограничивает выбор
};

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination: function () {
        this._super.apply(this, arguments);
        VariantMixin._onChangeCombinationPeriod.apply(this, arguments);
    },
});
