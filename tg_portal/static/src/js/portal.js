/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import "@portal/js/portal";

publicWidget.registry.portalDetails.include({
    events: Object.assign({}, publicWidget.registry.portalDetails.prototype.events, {
        "change #has_cedula": "_onHasCedulaChange",
    }),

    _onHasCedulaChange: function (ev) {
        if (ev.target.checked) {
            this.$el.find("label[for=cedula]").removeClass("invisible");
            this.$el.find("input[name=cedula]").removeClass("invisible");
        } else {
            this.$el.find("label[for=cedula]").addClass("invisible");
            this.$el.find("input[name=cedula]").addClass("invisible");
        }
    },
});
