from . import models


ALLOWED_DUPLICATE_TYPES = ("invoice", "delivery", "other")


def post_load():
    try:
        from odoo.addons.partner_email_check.models.res_partner import (
            api,
            _,
            UserError,
            ResPartner,
        )
    except ImportError:
        return

    from odoo.addons.auth_signup.models.res_users import SignupError

    @api.constrains("email")
    def _check_email_unique(self):
        if self._should_filter_duplicates():
            domains = self.sudo().env["partner.email.check.ignore"]._fetch_all_with_at()
            for rec in self.filtered("email"):
                if "," in rec.email:
                    raise UserError(
                        _(
                            "Field contains multiple email addresses. This is "
                            "not supported when duplicate email addresses are "
                            "not allowed."
                        )
                    )
                # <--- changes start

                if any([rec.email.endswith(x) for x in domains]):
                    continue

                already_in_use = False
                if self.env.context.get("no_reset_password"):
                    if (
                        self.sudo()
                        .env["res.users"]
                        .search_count([("email", "=", rec.email)])
                    ):
                        already_in_use = True
                elif rec.type not in ALLOWED_DUPLICATE_TYPES:
                    if self.search_count(
                        [
                            ("email", "=", rec.email),
                            ("id", "!=", rec.id),
                            ("type", "not in", ALLOWED_DUPLICATE_TYPES),
                        ]
                    ):
                        already_in_use = True

                if already_in_use:
                    raise SignupError(
                        _("Email '%s' is already in use.") % rec.email.strip()
                    )
                # <--- changes end

    ResPartner._check_email_unique = _check_email_unique
