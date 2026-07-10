/** @odoo-module **/

import {registry} from "@web/core/registry";
import wsTourUtils from "@website_sale/js/tours/tour_utils";

const DISCOUNT_CODE = "test_10pc"; // Make sure it is equal in tests

function makeSteps(expectedAmount) {
    return [
        {
            content: "Go to the `Events` page",
            trigger:
                'a[href*="/event"]:contains("Conference for Architects TEST"):first',
        },
        {
            content: "Open the register modal",
            trigger: 'button:contains("Register")',
        },
        {
            content: "Select 1 unit of `Standard` ticket type",
            extra_trigger:
                '#wrap:not(:has(a[href*="/event"]:contains("Conference for Architects")))',
            trigger: "select:eq(0)",
            run: "text 1",
        },
        {
            content: "Click on `Order Now` button",
            extra_trigger: "select:eq(0):has(option:contains(1):propSelected)",
            trigger: '.btn-primary:contains("Register")',
        },
        {
            content: "Fill attendees details",
            trigger: 'form[id="attendee_registration"] .btn[type=submit]',
            run: function () {
                $("input[name*='1-name']").val("Name Surname");
                $("input[name*='1-phone']").val("111 111");
                $("input[name*='1-email']")
                    .val("example@example.com")
                    .trigger("change");
            },
        },
        {
            content: "Validate attendees details",
            extra_trigger:
                "input[name*='1-name'], input[name*='2-name'], input[name*='3-name']",
            trigger: "button[type=submit]",
        },
        wsTourUtils.goToCart({quantity: 1}),
        wsTourUtils.goToCheckout(),
        ...wsTourUtils.assertCartAmounts({
            untaxed: expectedAmount,
        }),
    ];
}

registry.category("web_tour.tours").add("panama_event_buy_tickets", {
    test: true,
    url: "/event",
    steps: () =>
        makeSteps("900.00").concat([
            {
                content: "insert discount code",
                extra_trigger: 'form[name="coupon_code"]',
                trigger: 'form[name="coupon_code"] input[name="promo"]',
                run: "text " + DISCOUNT_CODE,
            },
            {
                content: "validate the promo code",
                trigger: 'form[name="coupon_code"] .a-submit',
            },
            {
                content: "check refused message",
                trigger: '.alert-danger:contains("This promo code is already applied")',
                isCheck: true,
            },
        ]),
});

registry
    .category("web_tour.tours")
    .add("not_panama_event_buy_tickets_and_try_apply_" + DISCOUNT_CODE, {
        test: true,
        url: "/event",
        steps: () =>
            makeSteps("1,000.00").concat([
                {
                    content: "insert discount code",
                    extra_trigger: 'form[name="coupon_code"]',
                    trigger: 'form[name="coupon_code"] input[name="promo"]',
                    run: "text " + DISCOUNT_CODE,
                },
                {
                    content: "validate the promo code",
                    trigger: 'form[name="coupon_code"] .a-submit',
                },
                {
                    content: "check refused message",
                    trigger:
                        '.alert-danger:contains("The program is not available for this order")',
                    isCheck: true,
                },
            ]),
    });
