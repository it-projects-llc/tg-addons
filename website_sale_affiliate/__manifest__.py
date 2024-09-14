# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

{
    "name": "Affiliate Program",
    "summary": "Create an e-commerce affiliate program for tracking referrals and conversions.",
    "version": "17.0.1.0.0",
    "category": "E-Commerce",
    "website": "https://github.com/it-projects-llc/tg-addons",
    "author": "LasLabs, Odoo Community Association (OCA), IT-Projects LLC",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "module_type": "official",
    "depends": [
        "website_sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sale_affiliate_data.xml",
        "views/sale_affiliate_view.xml",
        "views/sale_affiliate_request_view.xml",
        "views/sale_order_view.xml",
    ],
    "demo": [
        "demo/sale_affiliate_demo.xml",
    ],
}
