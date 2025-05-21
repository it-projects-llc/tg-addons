{
    "name": """Online Event Ticketing customizations for Tribal Gathering""",
    "version": "17.0.0.2.1",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "website_event_sale",
        "tg_website_sale_affiliate",
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "views/sale_affiliate_views.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_tests": [
            "tg_website_event_sale/static/tests/**/*",
        ],
    },
    "qweb": [],
}
