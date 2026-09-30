/** @odoo-module **/

import VariantMixin from "@website_sale/js/sale_variant_mixin";
import publicWidget from "@web/legacy/js/public/public_widget";

import "@website_sale/js/website_sale";

VariantMixin._onChangeCombinationPeriod = function (ev, $parent, combination) {
    let triggerChange = false;
    if (combination.start_date) {
        triggerChange = true;
        $parent.find("input[name=renting_start_date]").val(combination.start_date);
    }

    if (combination.end_date) {
        triggerChange = true;
        $parent.find("input[name=renting_end_date]").val(combination.end_date);
    }

    if (triggerChange) {
        $parent.find("input[name=renting_start_date]").trigger("change");
        $parent.find("input[name=renting_end_date]").trigger("change");
    }

    // TODO: не работает
};

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination: function () {
        this._super.apply(this, arguments);
        VariantMixin._onChangeCombinationPeriod.apply(this, arguments);
    },
});
