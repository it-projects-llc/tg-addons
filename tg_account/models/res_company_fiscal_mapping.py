from odoo import fields, models


class CompanyFiscalMappingJournal(models.Model):
    _name = "res.company.fiscal.mapping.journal"
    _description = "Company Fiscal Mapping Journal"

    company_from = fields.Many2one("res.company", required=True)
    company_to = fields.Many2one(related="company_from.fiscal_company", required=True)

    journal_from = fields.Many2one(
        "account.journal", domain="[('company_id', '=', company_from)]", required=True
    )
    journal_to = fields.Many2one(
        "account.journal", domain="[('company_id', '=', company_to)]", required=True
    )


class CompanyFiscalMappingAccount(models.Model):
    _name = "res.company.fiscal.mapping.account"
    _description = "Company Fiscal Mapping Account"

    company_from = fields.Many2one("res.company", required=True)
    company_to = fields.Many2one(related="company_from.fiscal_company", required=True)

    account_from = fields.Many2one(
        "account.account", domain="[('company_id', '=', company_from)]", required=True
    )
    account_to = fields.Many2one(
        "account.account", domain="[('company_id', '=', company_to)]", required=True
    )


class CompanyFiscalMappingTax(models.Model):
    _name = "res.company.fiscal.mapping.tax"
    _description = "Company Fiscal Mapping Tax"

    company_from = fields.Many2one("res.company", required=True)
    company_to = fields.Many2one(related="company_from.fiscal_company", required=True)

    tax_from = fields.Many2one(
        "account.tax", domain="[('company_id', '=', company_from)]", required=True
    )
    tax_to = fields.Many2one(
        "account.tax", domain="[('company_id', '=', company_to)]", required=True
    )


class CompanyFiscalMappingBankAccount(models.Model):
    _name = "res.company.fiscal.mapping.bank.account"
    _description = "Company Fiscal Mapping Bank Account"

    company_from = fields.Many2one("res.company", required=True)
    company_to = fields.Many2one(related="company_from.fiscal_company", required=True)

    bank_account_from = fields.Many2one(
        "res.partner.bank", domain="[('company_id', '=', company_from)]", required=True
    )
    bank_account_to = fields.Many2one(
        "res.partner.bank", domain="[('company_id', '=', company_to)]", required=True
    )


class CompanyFiscalMappingPaymentTerms(models.Model):
    _name = "res.company.fiscal.mapping.payment.term"
    _description = "Company Fiscal Mapping Payment Term"

    company_from = fields.Many2one("res.company", required=True)
    company_to = fields.Many2one(related="company_from.fiscal_company", required=True)

    payment_term_from = fields.Many2one(
        "account.payment.term",
        domain="[('company_id', '=', company_from)]",
        required=True,
    )
    payment_term_to = fields.Many2one(
        "account.payment.term",
        domain="[('company_id', 'in', [False, company_to])]",
        required=True,
    )
