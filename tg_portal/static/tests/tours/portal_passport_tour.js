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

function portalAccountSteps({hasCedula}) {
    const steps = [
        {
            content: "Open account details",
            trigger: 'a[href*="/my/account"]:contains("Edit"):first',
            run: "click",
        },
        {
            content: "Check the initial account details",
            trigger: "form[action='/my/account']",
            run: () => {
                const passport = document.querySelector('input[name="passport"]');
                const cedula = document.querySelector('input[name="cedula"]');
                const hasCedulaInput = document.querySelector(
                    'input[name="has_cedula"]'
                );
                const birthdate = document.querySelector(
                    'input[name="birthdate_date"]'
                );
                const nationality = document.querySelector(
                    'select[name="nationality_id"]'
                );
                if (
                    passport.value ||
                    birthdate.value ||
                    nationality.value ||
                    hasCedulaInput.checked
                ) {
                    throw new Error("Identification fields are not initially empty");
                }
                if (!cedula.classList.contains("invisible")) {
                    throw new Error("Cedula is visible while its checkbox is unchecked");
                }
            },
        },
    ];

    if (hasCedula) {
        steps.push(
            {
                content: "Check 'I have Cedula'",
                trigger: 'input[name="has_cedula"]',
                run: () => {
                    $('input[name="has_cedula"]').prop("checked", true).trigger("change");
                },
            },
            {
                content: "Ensure Cedula is visible",
                trigger: 'input[name="cedula"]:not(.invisible)',
                isCheck: true,
            }
        );
    }

    steps.push(
        {
            content: "Submit the incomplete account form",
            trigger: "button[type=submit]",
            run: "click",
            extra_trigger: "form[action='/my/account']",
        },
        ...(
            hasCedula
                ? [
                      ["cedula", "Cedula"],
                      ["birthdate_date", "Date of Birth"],
                      ["nationality_id", "Country of Citizenship"],
                  ]
                : [
                      ["passport", "Passport"],
                      ["birthdate_date", "Date of Birth"],
                      ["nationality_id", "Country of Citizenship"],
                  ]
        ).map(([field, label]) => ({
            content: `Ensure ${label} is highlighted as required`,
            trigger: `form[action='/my/account'] [name="${field}"].is-invalid`,
            isCheck: true,
        }))
    );

    return steps;
}

registry.category("web_tour.tours").add("tg_portal.portal_account_required_without_cedula", {
    test: true,
    url: "/my",
    steps: () => portalAccountSteps({hasCedula: false}),
});

registry.category("web_tour.tours").add("tg_portal.portal_account_required_with_cedula", {
    test: true,
    url: "/my",
    steps: () => portalAccountSteps({hasCedula: true}),
});
