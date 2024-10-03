{
    "name": """Signup modifications for Tribal Gathering""",
    "version": "17.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "auth_signup",
        "website",  # required at least for running tests
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/auth_signup_login_templates.xml",
    ],
}
