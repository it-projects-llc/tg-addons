{
    "name": """Signup modifications for Tribal Gathering""",
    "version": "14.0.0.1.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://www.it-projects.info",
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
