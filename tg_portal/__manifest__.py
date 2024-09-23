{
    "name": """Portal modifications for Tribal Gathering""",
    "version": "17.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "portal",
        "partner_contact_nationality",
        "partner_identification",
        "partner_contact_birthdate",
    ],
    "data": [
        "views/portal_templates.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "tg_portal/static/src/js/portal.js",
        ],
    },
}
