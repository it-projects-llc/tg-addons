{
    "name": """Portal modifications for Tribal Gathering""",
    "version": "17.0.0.1.2",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "portal",
        "sign",
        "sale",
        "partner_contact_nationality",
        "partner_identification",
        "partner_contact_birthdate",
    ],
    "data": [
        "views/sign_portal_templates.xml",
        "views/sale_portal_templates.xml",
        "views/portal_templates.xml",
        "views/res_partner_views.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "tg_portal/static/src/js/portal.js",
            "tg_portal/static/src/scss/portal_menu.scss",
        ],
    },
}
