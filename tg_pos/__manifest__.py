{
    "name": """Point of Sale modifications for Tribal Gathering""",
    "version": "17.0.0.3.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "tg_account",
        "point_of_sale",
        "pos_partner_deselection",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "security/point_of_sale_security.xml",
        "views/account_move_views.xml",
        "views/product_view.xml",
        "views/pos_session_views.xml",
        "views/pos_shop_views.xml",
        "views/res_config_settings_views.xml",
        "wizard/generate_grouped_invoice_views.xml",
    ],
    "demo": [],
    "assets": {
        "point_of_sale._assets_pos": [
            "tg_pos/static/src/**/*",
        ],
        "web.assets_tests": [
            "tg_pos/static/tests/tours/pos_customer_button_tour.js",
        ],
    },
    "post_load": "post_load",
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
