/** @odoo-module **/

import {registry} from "@web/core/registry";
import wsTourUtils from "@website_sale/js/tours/tour_utils";

function openEventByName(name) {
    return {
        content: "Open event " + name,
        trigger: '.o_wevent_events_list a:contains("' + name + '")',
    };
}

const OTHER_STEPS_UNTIL_CART = [
    {
        content: "Open Registration Page",
        trigger: '.btn-primary:contains("Register")',
    },
    {
        content: "Select 1 units of `Standart` ticket type",
        trigger: "#o_wevent_tickets select.form-select",
        run: "text 1",
    },
    {
        content: "Click on `Register` button",
        trigger: '#o_wevent_tickets button:contains("Register")',
    },
    {
        content: "Fill attendees details",
        trigger: 'form[id="attendee_registration"] .btn[type=submit]',
        run: function () {
            $("input[name*='1-email']").val("att1@example.com").trigger("change");
            $("input[name*='1-name']").val("Att1");
            $("input[name*='1-phone']").val("111 111");
        },
    },
    {
        content: "Validate attendees details",
        extra_trigger: "input[name*='1-name']",
        trigger: "button[type=submit]",
    },
];

registry
    .category("web_tour.tours")
    .add("tg_website_event_sale_create_event1_registration", {
        test: true,
        url: "/event",
        steps: () =>
            [openEventByName("Pycon")]
                .concat(OTHER_STEPS_UNTIL_CART)
                .concat([wsTourUtils.goToCart({quantity: 1})]),
    });

registry
    .category("web_tour.tours")
    .add("tg_website_event_sale_create_event2_registration", {
        test: true,
        url: "/event",
        steps: () =>
            [openEventByName("Conference for Architects TEST")]
                .concat(OTHER_STEPS_UNTIL_CART)
                .concat([wsTourUtils.goToCart({quantity: 1})]),
    });

registry.category("web_tour.tours").add("tg_website_event_sale_change_ticket", {
    test: true,
    steps: () =>
        [
            {
                content: "Click on `Upgrade/change ticket` button",
                trigger: "a[data-bs-target='#changeTicketModal']",
            },
            {
                content: "Click submit on modal",
                trigger: "form button[type='submit']",
            },
        ]
            .concat(OTHER_STEPS_UNTIL_CART)
            .concat([wsTourUtils.goToCart({quantity: 3})]),
});
