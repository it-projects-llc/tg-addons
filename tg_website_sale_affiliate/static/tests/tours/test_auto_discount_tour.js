/** @odoo-module **/

import {registry} from "@web/core/registry";
import tourUtils from "@website_sale/js/tours/tour_utils";

registry.category("web_tour.tours").add("tg_auto_set_discount_by_affiliate", {
    test: true,
    url: "/shop?search=Small%20Cabinet",
    steps: () => [
        {
            content: "select Small Cabinet",
            extra_trigger: ".oe_search_found",
            trigger: '.oe_product_cart a:contains("Small Cabinet")',
        },
        {
            content: "add 2 Small Cabinet into cart",
            trigger: '#product_details input[name="add_qty"]',
            run: "text 2",
        },
        {
            content: "click on 'Add to Cart' button",
            trigger: "a:contains(Add to cart)",
        },
        tourUtils.goToCart({quantity: 2}),
        {
            content: "check reward product",
            trigger: 'div>strong:contains("10.0% discount on total amount")',
            run: function () {
                // It's a check
            },
        },
        {
            content: "go to checkout",
            trigger: 'a[href="/shop/checkout?express=1"]',
        },
        ...tourUtils.assertCartAmounts({
            total: "180.00",
        }),
    ],
});
