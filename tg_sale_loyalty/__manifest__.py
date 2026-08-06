{
    "name": """Sale Loyalty modifications for Tribal Gathering""",
    "version": "17.0.0.3.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "sale_loyalty",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/product_template_views.xml",
        "views/loyalty_program_views.xml",
    ],
    "demo": [],
    "post_load": "post_load",
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
