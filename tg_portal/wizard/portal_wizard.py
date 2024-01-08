from odoo import models

from odoo.addons.portal.wizard.portal_wizard import extract_email


class PortalWizard(models.TransientModel):
    _inherit = "portal.wizard.user"

    # based on original _create_user from same wizard
    def _create_user(self):
        user = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            ._create_user_from_template(
                {
                    "email": extract_email(self.email),
                    "login": extract_email(self.email),
                    "partner_id": self.partner_id.id,
                }
            )
        )
        user.write(
            {
                "company_id": self.env.company.id,
                "company_ids": [(4, self.env.company.id)],
            }
        )
        return user
