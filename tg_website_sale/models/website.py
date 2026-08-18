from odoo import _, models


class Website(models.Model):
    _inherit = "website"

    def _display_partner_b2b_fields(self):
        return False

    # based on account.move._search_default_journal
    def _action_show_sale_journals(self):
        self.ensure_one()

        journal_types = ["sale"]
        company = self.company_id
        domain = [
            *self.env["account.journal"]._check_company_domain(company),
            ("type", "in", journal_types),
        ]

        return {
            "name": _("Journals"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "account.journal",
            "domain": domain,
        }
