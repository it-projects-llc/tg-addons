{
    "name": """Marketing fields in Contact""",
    "version": "17.0.0.3.0",
    "author": "IT-Projects LLC",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "contacts",
        "auth_signup",
        "sales_team",
        "website_event",
    ],
    "data": [
        "views/event_templates.xml",
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/contact_views.xml",
        "wizard/marketing_answer_merge_views.xml",
    ],
    "demo": ["data/event_question_demo.xml"],
    "qweb": [],
}
