{
    "name": """eCommerce Rental modifications for Tribal Gathering""",
    "version": "17.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "Other proprietary",  # pylint: disable=license-allowed
    "depends": [
        "website_sale_renting",
    ],
    "assets": {
        "web.assets_frontend": [
            "tg_website_sale_renting/static/src/js/*.js",
        ],
    },
    "data": [
        "views/templates.xml",
        "views/res_config_settings_views.xml",
    ],
    "demo": [],
}
