{
    "name": """Affiliate Program customizations for Tribal Gathering""",
    "version": "17.0.0.2.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": ["website_sale_affiliate", "website_sale_loyalty"],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template_data.xml",
        "views/loyalty_program_views.xml",
        "views/portal_templates.xml",
        "views/res_partner_views.xml",
        "views/sale_affiliate_views.xml",
        "views/menus.xml",
    ],
    "assets": {
        "web.assets_tests": [
            "tg_website_sale_affiliate/static/tests/**/*",
        ],
    },
    "demo": [],
    "qweb": [],
}
