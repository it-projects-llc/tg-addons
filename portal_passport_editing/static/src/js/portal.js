odoo.define('portal_passport_editing.portal', function (require) {
    'use strict';

    require("portal.portal");
    var publicWidget = require('web.public.widget');

    publicWidget.registry.portalDetails.include({
        events: _.extend({}, publicWidget.registry.portalDetails.prototype.events, {
            'change #has_cedula': '_onHasCedulaChange',
        }),

        _onHasCedulaChange: function(ev) {
            if (ev.target.checked) {
                this.$el.find("label[for=cedula]").removeClass("d-none");
                this.$el.find("input[name=cedula]").removeClass("d-none");
            } else {
                this.$el.find("label[for=cedula]").addClass("d-none");
                this.$el.find("input[name=cedula]").addClass("d-none");
            }
        },
    });
});
