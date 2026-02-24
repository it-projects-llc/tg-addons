from odoo import fields, models


class PartnerEmailCheckIgnore(models.Model):
    _name = "partner.email.check.ignore"
    _description = "Email check ignore record"
    _rec_name = "domain"

    domain = fields.Char(required=True)

    _sql_constraints = [
        (
            "unique_name",
            "UNIQUE(domain)",
            "Another record with the same domain already exists.",
        )
    ]

    def _fetch_all_with_at(self):
        records = self.search([])
        if not records:
            return set()
        return set(self.search([]).mapped(lambda x: "@" + x.domain.strip()))
