{
    "name": """Split payments for Online ticketing""",
    "version": "17.0.0.3.0",
    "author": "IT-Projects LLC, Eugene Molotov",
    "support": "it@it-projects.info",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "license": "AGPL-3",
    "depends": [
        "website_event_sale",
        "tg_sale_invoice_plan",
    ],
    "data": [
        "views/event_ticket_views.xml",
        "data/ir_config_parameter_data.xml",
        "views/event_registration_views.xml",
        "views/res_config_settings_views.xml",
        "views/website_sale_templates.xml",
        "report/invoice_plan_report.xml",
        "report/invoice_plan_report_templates.xml",
        "data/mail_template_data.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "tg_website_event_sale_split_payments/static/src/**/*",
        ],
        "web.assets_tests": [
            "tg_website_event_sale_split_payments/static/tests/**/*",
        ],
    },
    "demo": [],
}
