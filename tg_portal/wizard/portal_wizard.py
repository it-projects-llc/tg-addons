from odoo import models
from odoo.tools import email_normalize


class PortalWizard(models.TransientModel):
    _inherit = "portal.wizard.user"

    # based on original _create_user from same wizard
    def _create_user(self):
        normalized_email = email_normalize(self.email)
        vals = {
            "email": normalized_email,
            "login": normalized_email,
            "partner_id": self.partner_id.id,
        }

        # When partner_email_check
        # creating user with duplicated email will be denied
        # we use this hack, to escape email duplicate checking
        if self.partner_id.email == vals["email"]:
            vals.pop("email")

        user = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            ._create_user_from_template(vals)
        )
        user.write(
            {
                "company_id": self.env.company.id,
                "company_ids": [(4, self.env.company.id)],
            }
        )
        return user
