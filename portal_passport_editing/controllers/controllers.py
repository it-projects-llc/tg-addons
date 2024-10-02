from odoo.addons.portal.controllers.portal import CustomerPortal


class website_account_passport(CustomerPortal):
    OPTIONAL_BILLING_FIELDS = CustomerPortal.OPTIONAL_BILLING_FIELDS + []
