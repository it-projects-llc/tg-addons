from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    fiscal_company = fields.Many2one(
        "res.company",
        domain="[('id', '!=', id)]",
        help="Company, where invoices will be manually duplicated",
    )

    fiscal_company_mapping_journal = fields.One2many(
        "res.company.fiscal.mapping.journal", "company_from"
    )
    fiscal_company_mapping_account = fields.One2many(
        "res.company.fiscal.mapping.account", "company_from"
    )
    fiscal_company_mapping_tax = fields.One2many(
        "res.company.fiscal.mapping.tax", "company_from"
    )
    fiscal_company_mapping_bank_account = fields.One2many(
        "res.company.fiscal.mapping.bank.account", "company_from"
    )
    fiscal_company_mapping_payment_term = fields.One2many(
        "res.company.fiscal.mapping.payment.term", "company_from"
    )
