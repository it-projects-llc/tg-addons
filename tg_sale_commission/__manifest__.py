{
    "name": """Sales commissions modifications for Tribal Gathering""",
    "version": "14.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "sale_commission",
        "tg_website_sale_affiliate",
    ],
    "external_dependencies": {
        "python": [
            "git+https://github.com/em230418/e-commerce@14.0-mig-website_sale_affiliate#subdirectory=setup/website_sale_affiliate"  # noqa: B950
        ]
    },
    "data": [
        "views/sale_affiliate_view.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [],
}
