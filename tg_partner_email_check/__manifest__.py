{
    "name": """Email checker modifications for Tribal Gathering""",
    "version": "17.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "auth_signup_verify_email",
        "partner_email_check",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/partner_email_check_ignore_views.xml",
    ],
    "demo": [],
    "post_load": "post_load",
}
