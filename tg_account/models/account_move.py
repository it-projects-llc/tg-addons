from odoo import fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    must_be_duplicated = fields.Boolean(
        groups="account.group_account_user",
        tracking=True,
    )
    duplicated_fiscal_invoice = fields.Many2one(
        "account.move",
        groups="account.group_account_user",
        tracking=True,
    )

    def _duplicate_invoice_check(self):
        no_fiscal_companies = []
        have_duplicated_invoice = []

        for move in self:
            if move.duplicated_fiscal_invoice:
                have_duplicated_invoice.append(move.name)
                continue

            fiscal_company = move.company_id.fiscal_company
            if not fiscal_company:
                no_fiscal_companies.append(move.name)
                continue

        error_msgs = []
        if no_fiscal_companies:
            error_msgs.append("No fiscal companies: " + ", ".join(no_fiscal_companies))

        if have_duplicated_invoice:
            error_msgs.append(
                "Already have duplicated invoices: "
                + ", ".join(have_duplicated_invoice)
            )

        if error_msgs:
            raise ValidationError("\n".join(error_msgs))

    def _duplicate_invoice_inner(self):
        new_move_ids = []
        for old_move in self:
            fiscal_company = old_move.company_id.fiscal_company
            allowed_company_ids = self.env.context.get("allowed_company_ids") + [
                fiscal_company.id
            ]
            new_move = old_move.with_context(
                allowed_company_ids=allowed_company_ids,
                duplicate_invoice_to_fiscal_company=fiscal_company.id,
            ).copy()
            old_move.duplicated_fiscal_invoice = new_move
            new_move_ids.append(new_move.id)

        return new_move_ids

    def _action_duplicate_to_fiscal_company(self):
        self._duplicate_invoice_check()

        new_move_ids = self._duplicate_invoice_inner()

        new_move = self.env["account.move"].browse(new_move_ids)[0]

        action = new_move.open_action()
        if len(new_move_ids) > 1:
            action["domain"] = [("id", "in", new_move_ids)]
        elif len(new_move_ids) == 1:
            form_view = [(self.env.ref("account.view_move_form").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = new_move_ids[0]
        else:
            action = {"type": "ir.actions.act_window_close"}

        return action

    def copy_data(self, default=None):
        data_list = super().copy_data(default)

        if not self.env.context.get("duplicate_invoice_to_fiscal_company"):
            return data_list

        fiscal_company_id = self.env.context.get("duplicate_invoice_to_fiscal_company")
        JournalMappings = self.sudo().env["res.company.fiscal.mapping.journal"]
        BankAccountMappings = self.sudo().env["res.company.fiscal.mapping.bank.account"]

        for move, data in zip(self, data_list, strict=False):
            data["company_id"] = fiscal_company_id

            new_journal = JournalMappings.search(
                [
                    ("company_from", "=", move.company_id.id),
                    ("company_to", "=", fiscal_company_id),
                    ("journal_from", "=", move.journal_id.id),
                ],
                limit=1,
            ).journal_to

            if new_journal:
                data["journal_id"] = new_journal.id

            new_bank_account = BankAccountMappings.search(
                [
                    ("company_from", "=", move.company_id.id),
                    ("company_to", "=", fiscal_company_id),
                    ("bank_account_from", "=", move.partner_bank_id.id),
                ],
                limit=1,
            ).bank_account_to

            data["partner_bank_id"] = new_bank_account.id

        return data_list
