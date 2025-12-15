{
    "name": """Combo tickets""",
    "version": "17.0.0.2.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "LGPL-3",
    "depends": [
        "website_event_sale",
        "website_event_questions_by_ticket",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/generate_shuttle_ticket_answers_views.xml",
        "views/event_question_views.xml",
        "views/templates.xml",
        "views/res_config_settings_views.xml",
        "views/event_ticket_views.xml",
        "views/event_event_views.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "tg_website_event_sale_combo_tickets/static/**/*",
        ]
    },
}
