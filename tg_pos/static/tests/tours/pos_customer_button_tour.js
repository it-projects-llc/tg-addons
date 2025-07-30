/** @odoo-module **/

import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("tg_pos.customer_button_visible", {
    test: true,
    url: "/pos/ui",
    steps: () => [
        {
            content: "Open POS",
            trigger: 'button[name="open_ui"]',
            run: "click",
        },
        {
            content: "Confirm and open POS session",
            trigger: '.btn.btn-primary:contains("Open session")',
            run: "click",
        },
        {
            content: "'Customer' button should not be disabled",
            trigger: ".button.set-partner",
            run: () => {
                const btn = document.querySelector(".button.set-partner");
                if (btn.hasAttribute("disabled")) {
                    throw new Error("'Customer' button should not be disabled");
                }
            },
        },
    ],
});

registry.category("web_tour.tours").add("tg_pos.customer_button_hidden", {
    test: true,
    url: "/pos/ui",
    steps: () => [
        {
            content: "Open POS",
            trigger: 'button[name="open_ui"]',
            run: "click",
        },
        {
            content: "'Customer' button should be disabled",
            trigger: ".set-partner",
            extra_trigger: ".product-screen",
            run: () => {
                const btn = document.querySelector(".button.set-partner");

                if (!btn) {
                    throw new Error("Customer button not found");
                }

                if (!btn.hasAttribute("disabled")) {
                    throw new Error("Customer button should be disabled");
                }
            },
            isCheck: true,
        },
    ],
});
