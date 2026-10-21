{
    "name": """Web modifications for Tribal Gathering""",
    "version": "17.0.0.2.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "web",
    ],
    "assets": {
        "web.assets_backend": [
            ("after", "web/static/src/core/**/*", "tg_web/static/src/views/**/*"),
        ],
    },
    "data": [],
    "demo": [],
}
