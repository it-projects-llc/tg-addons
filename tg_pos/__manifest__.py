{
    "name": """Point of Sale modifications for Tribal Gathering""",
    "version": "14.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://www.it-projects.info",
    "license": "LGPL-3",
    "depends": [
        'point_of_sale',
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/point_of_sale_security.xml",
        'views/assets.xml',
    ],
    "demo": [
    ],
    "qweb": [
        "static/src/xml/Screens/PaymentScreen/PaymentScreen.xml",
        "static/src/xml/Screens/ProductScreen/ActionpadWidget.xml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,
}
