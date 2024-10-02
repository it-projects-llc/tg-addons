import logging

from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal, _

_logger = logging.getLogger(__name__)


TG_BASE_AGPL_FIELDS = [
    "passport",
    "birthdate_date",
    "nationality_id",
    "cedula",
    "has_cedula",
]


class TGCustomerPortal(CustomerPortal):
    def _get_optional_fields(self):
        res = super()._get_optional_fields()
        res += TG_BASE_AGPL_FIELDS + [
            "is_passport_not_ready",
        ]
        partner_fields = request.env["res.partner"]._fields
        for fname in TG_BASE_AGPL_FIELDS:
            if fname not in partner_fields:
                raise Exception(
                    f"Missing field {fname}. Probably tg_base_agpl is not installed"
                )
        return res

    @route()
    def account(self, redirect=None, **post):
        if post.get("nationality_id"):
            post["nationality_id"] = int(post["nationality_id"])

        res = super().account(redirect, **post)
        res.qcontext["show_passport_checkbox"] = (
            "event_guest" in request.env.user._fields
        )
        return res

    def details_form_validate(self, data):
        res = super().details_form_validate(data)
        for fname in ("is_passport_not_ready", "has_cedula"):
            data[fname] = data.get(fname, False)

        for fname in ("passport", "cedula"):
            data[fname] = data[fname].strip()

        if "event_guest" not in request.env.user._fields:
            return res

        is_something_extra_missing = False
        error, error_message = res
        ignore_passport = bool(data["cedula"]) or request.env.user.has_group(
            "base.group_user"
        )

        if (
            not ignore_passport
            and not data["is_passport_not_ready"]
            and not data["passport"].strip()
        ):
            error["passport"] = "missing"
            is_something_extra_missing = True

        if not data["cedula"] and data.get("has_cedula"):
            error["cedula"] = "missing"
            is_something_extra_missing = True

        if not data["birthdate_date"]:
            error["birthdate_date"] = "missing"
            is_something_extra_missing = True

        if not data["nationality_id"]:
            error["nationality_id"] = "missing"
            is_something_extra_missing = True

        if not data["cedula"] and data["has_cedula"]:
            error["cedula"] = "missing"
            is_something_extra_missing = True

        if is_something_extra_missing:
            missing_error_message = _("Some required fields are empty.")
            if missing_error_message not in error_message:
                error_message.append(missing_error_message)

        return error, error_message
