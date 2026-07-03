from odoo import fields, models


class AlreadyDuplicatedInvoicesWizard(models.TransientModel):
    _name = "already.duplicated.invoices.wizard"
    _description = "Already duplicated invoices wizard"

    invoices_to_duplicate = fields.Many2many(
        "account.move", "adiw_invoices_to_duplicate_rel", readonly=True
    )
    already_duplicated_invoices = fields.Many2many(
        "account.move",
        "adiw_already_duplicated_invoices_rel",
        readonly=True,
    )

    def action_ignore_and_duplicate(self):
        self.ensure_one()
        return self.invoices_to_duplicate._action_duplicate_to_fiscal_company()
