/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("tg_portal.portal_passport_tour", {
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
            content: "Enter Birthdate",
            trigger: 'input[name="birthdate_date"]',
            run: () => {
                document.querySelector('input[name="birthdate_date"]').value =
                    "2000-01-01";
            },
        },
        {
            content: "Enter Nationality",
            trigger: 'select[name="nationality_id"]',
            run: () => {
                $('select[name="nationality_id"] option:eq(1)').attr("selected", true);
            },
        },
        {
            content: "Submit the form",
            trigger: "button[type=submit]",
            run: "click",
            extra_trigger: "form[action='/my/account']",
        },
        {
            content: "Ensure we returned to portal home",
            trigger: 'a[href*="/my/account"]:contains("Edit"):first',
            extra_trigger: "div.o_portal_my_details",
            isCheck: true,
        },
    ],
});
