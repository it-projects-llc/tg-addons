# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Sales Invoice Plan modifications for Tribal Gathering",
    "summary": "Add to sales order, ability to manage future invoice plan",
    "version": "17.0.1.0.0",
    "author": "Ecosoft,Odoo Community Association (OCA),IT-Projects LLC",
    "license": "AGPL-3",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "category": "Sales",
    "depends": ["account", "sale_management"],
    "excludes": ["sale_invoice_plan"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sale_create_invoice_plan_view.xml",
        "wizard/sale_make_planned_invoice_view.xml",
        "views/sale_view.xml",
    ],
}
