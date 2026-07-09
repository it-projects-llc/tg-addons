{
    "name": """Coupons, Promotions, Gift Card and Loyalty for eCommerce
    modifications for Tribal Gathering""",
    "version": "17.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "partner_contact_nationality",
        "website_event_sale",
        "website_sale_loyalty",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/loyalty_security.xml",
        "views/nationality_discount_program_views.xml",
        "views/loyalty_program_views.xml",
        "views/menuitems.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_tests": [
            "tg_website_sale_loyalty/static/tests/**/*",
        ],
    },
}
