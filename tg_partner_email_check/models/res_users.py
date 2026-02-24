from odoo import api, models
from odoo.tools import email_normalize


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def _signup_create_user(self, values):
        Partner = self.env["res.partner"].sudo()
        if "partner_id" not in values:
            email = email_normalize(values["login"])
            domain = [
                ("email", "=", email),
                ("type", "=", "contact"),
            ]
            if values.get("company_id"):
                domain += [("company_id", "in", (False, values["company_id"]))]
            else:
                domain += [("company_id", "=", False)]
            partners = Partner.search(domain, order="id DESC")
            if len(partners) == 1:
                values["partner_id"] = partners.id
            elif len(partners) > 1:
                partner_id = partners[0].id

                if "credit_balance" in partners._fields:
                    # pos_debt_notebook is used
                    # using that one, with greatest balance
                    partners.mapped("credit_balance")
                    largest_credit = partners[0].credit_balance
                    for p in partners[1:]:
                        if p.credit_balance > largest_credit:
                            largest_credit = p.credit_balance
                            partner_id = p.id

                values["partner_id"] = partner_id

        return super()._signup_create_user(values)
