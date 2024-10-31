{
    "name": """Point of Sale modifications for Tribal Gathering""",
    "version": "17.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "point_of_sale",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/point_of_sale_security.xml",
    ],
    "demo": [],
    "assets": {
        "point_of_sale._assets_pos": [
            "tg_pos/static/src/**/*",
        ],
    },
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
