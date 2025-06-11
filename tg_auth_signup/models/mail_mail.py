from odoo import _, api, models


class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("subject") == _("Password reset"):
                website = self.env["website"].get_current_website()
                if website.company_id.email_formatted:
                    vals["email_from"] = website.company_id.email_formatted

        return super().create(vals_list)
