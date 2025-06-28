/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("portal_passport_tour", {
    test: true,
    url: "/my",
    steps: () => [
        {
            content: "Click Edit",
            trigger: 'a[href*="/my/account"]:contains("Edit"):first',
        },
        {
            content: "Check 'I have Cedula' if not already checked",
            trigger: 'input[name="has_cedula"]',
            run: () => {
                $('input[name="has_cedula"]').prop("checked", true).trigger("change");
            },
        },
        {
            content: "Enter Cedula",
            trigger: 'input[name="cedula"]',
            run: "text CedulaTest",
        },
        {
            content: "Enter Passport",
            trigger: 'input[name="passport"]',
            run: "text PassportTest",
        },
        {
            content: "Submit the form",
            trigger: "button[type=submit]",
        },
        {
            content: "Check that we are back on the portal",
            trigger: 'a[href*="/my/account"]:contains("Edit"):first',
            isCheck: true,
        },
    ],
});
