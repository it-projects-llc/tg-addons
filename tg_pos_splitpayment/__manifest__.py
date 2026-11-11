{
    "name": "POS Split Payment",
    "version": "17.0.1.0.0",
    "author": "IT-Projects LLC",
    "license": "LGPL-3",
    "depends": ["point_of_sale", "pos_restaurant"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "tg_pos_splitpayment/static/src/**/*",
        ],
    },
    "installable": True,
}
