{
    "name": """RFID adapter for POSes""",
    "summary": """Converts RFID scan result to a proper value""",
    "category": "Point of Sale",
    "version": "17.0.1.0.0",
    "author": "IT-Projects LLC",
    "support": "apps@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "point_of_sale",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_rfid/static/src/**/*",
        ],
    },
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "demo": [
        "data/point_of_sale_demo.xml",
    ],
}
