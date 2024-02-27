# -*- coding: utf-8 -*-
# Copyright 2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.addons.portal.controllers.portal import CustomerPortal, _
from odoo.http import route, request


class website_account_passport(CustomerPortal):

    OPTIONAL_BILLING_FIELDS = CustomerPortal.OPTIONAL_BILLING_FIELDS + ["passport", "is_passport_not_ready", "birthdate_date", "nationality_id"]

    @route()
    def account(self, redirect=None, **post):
        res = super(website_account_passport, self).account(redirect, **post)
        res.qcontext["show_passport_checkbox"] = "event_guest" in request.env.user._fields
        return res

    def details_form_validate(self, data):
        is_passport_not_ready = data.get("is_passport_not_ready", False)
        res = super(website_account_passport, self).details_form_validate(data)

        if "event_guest" not in request.env.user._fields:
            return res

        is_something_extra_missing = False
        error, error_message = res
        if not is_passport_not_ready and not data["passport"].strip():
            error["passport"] = "missing"
            is_something_extra_missing = True

        if not data["birthdate_date"]:
            error["birthdate_date"] = "missing"
            is_something_extra_missing = True

        if not data["nationality_id"]:
            error["nationality_id"] = "missing"
            is_something_extra_missing = True

        if is_something_extra_missing:
            missing_error_message = _('Some required fields are empty.')
            if missing_error_message not in error_message:
                error_message.append(missing_error_message)

        return error, error_message
