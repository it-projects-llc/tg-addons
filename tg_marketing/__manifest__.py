{
    "name": """Marketing fields in Contact""",
    "version": "17.0.0.4.0",
    "author": "IT-Projects LLC",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "contacts",
        "auth_signup",
        "sales_team",
        "website_event_attendee_fields",
    ],
    "data": [
        "data/ir_model_data.xml",
        "views/event_templates_page_registration.xml",
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/contact_views.xml",
        "wizard/marketing_answer_merge_views.xml",
    ],
    "demo": ["data/event_question_demo.xml"],
    "qweb": [],
}
