/** @odoo-module **/

import EventRegistrationForm from "@website_event/js/website_event";

EventRegistrationForm.include({
    on_click: function () {
        return this._super.apply(this, arguments).then(function () {
            $(
                "form#attendee_registration .modal-body select[data-shuttle-price-warning]"
            ).on("change", function (ev) {
                const selector = $(ev.target).data("shuttle-price-warning");
                if (
                    $("select[data-shuttle-price-warning]")
                        .map((i, x) => x.value)
                        .get()
                        .some(Boolean)
                ) {
                    $(selector).show("slow");
                } else {
                    $(selector).hide("slow");
                }
            });
        });
    },
});
