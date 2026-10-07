{
    "name": "eCommerce Rental Period Attributes",
    "version": "17.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "Other proprietary",  # pylint: disable=license-allowed
    "depends": [
        "tg_website_sale_renting",
    ],
    "assets": {
        "web.assets_frontend": [
            "tg_website_sale_renting_attributes/static/src/js/*.js",
        ],
    },
    "data": [
        "views/templates.xml",
        "views/product_attribute_views.xml",
        "views/product_template_views.xml",
    ],
    "demo": [],
}
