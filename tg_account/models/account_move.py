from odoo import api, fields, models
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
    is_duplicated_invoice = fields.Boolean(
        compute="_compute_is_duplicated_invoice", store=False
    )
    show_fiscal_related_fields = fields.Boolean(
        compute="_compute_show_fiscal_related_fields"
    )

    def _compute_show_fiscal_related_fields(self):
        for record in self:
            record.show_fiscal_related_fields = bool(record.company_id.fiscal_company)

    def _compute_is_duplicated_invoice(self):
        self.env.cr.execute(
            """
SELECT array_agg(DISTINCT duplicated_fiscal_invoice)
FROM account_move
WHERE duplicated_fiscal_invoice IN %s
        """,
            [tuple(self.ids)],
        )
        duplicated_invoice_ids = self.env.cr.fetchone()[0] or []
        for move in self:
            move.is_duplicated_invoice = move.id in duplicated_invoice_ids

    @api.onchange("duplicated_fiscal_invoice")
    def _onchange_duplicated_fiscal_invoice(self):
        if (
            not self.duplicated_fiscal_invoice
            and self._origin.duplicated_fiscal_invoice
        ):
            self.must_be_duplicated = True

    def _duplicate_invoice_check(self):
        no_fiscal_companies = []
        have_duplicated_invoice = []

        for move in self:
            if move.duplicated_fiscal_invoice:
                have_duplicated_invoice.append(move.display_name)
                continue

            fiscal_company = move.company_id.fiscal_company
            if not fiscal_company:
                no_fiscal_companies.append(move.display_name)
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
            old_move.must_be_duplicated = False
            new_move_ids.append(new_move.id)

        return new_move_ids

    def _action_duplicate_to_fiscal_company(self):
        already_duplicated = self.filtered("duplicated_fiscal_invoice")

        if already_duplicated:
            w = self.env["already.duplicated.invoices.wizard"].create(
                {
                    "invoices_to_duplicate": [(6, 0, (self - already_duplicated).ids)],
                    "already_duplicated_invoices": [(6, 0, already_duplicated.ids)],
                }
            )
            return {
                "name": "Duplicated invoices",
                "type": "ir.actions.act_window",
                "res_model": "already.duplicated.invoices.wizard",
                "view_mode": "form",
                "res_id": w.id,
                "target": "new",
            }

        self._duplicate_invoice_check()

        new_move_ids = self._duplicate_invoice_inner()

        move_types = list(set(self.mapped("move_type")))
        if len(move_types) == 1 and move_types[0] != "entry":
            action_xmlid = "account.action_move_" + move_types[0] + "_type"
        else:
            action_xmlid = "account.action_move_journal_line"

        action = self.env["ir.actions.actions"]._for_xml_id(action_xmlid)

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
        PaymentTermMappings = self.sudo().env["res.company.fiscal.mapping.payment.term"]
        invoice_date = self.invoice_date
        invoice_date_due = self.invoice_date_due

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

            new_payment_term = PaymentTermMappings.search(
                [
                    ("company_from", "=", move.company_id.id),
                    ("company_to", "=", fiscal_company_id),
                    ("payment_term_from", "=", move.invoice_payment_term_id.id),
                ],
                limit=1,
            ).payment_term_to

            if new_payment_term:
                data["invoice_payment_term_id"] = new_payment_term.id

            new_bank_account = BankAccountMappings.search(
                [
                    ("company_from", "=", move.company_id.id),
                    ("company_to", "=", fiscal_company_id),
                    ("bank_account_from", "=", move.partner_bank_id.id),
                ],
                limit=1,
            ).bank_account_to

            data["partner_bank_id"] = new_bank_account.id

            data["invoice_date"] = invoice_date

            data["invoice_date_due"] = invoice_date_due

        return data_list

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == "tree" and not self.env.company.show_fiscal_related_columns:
            for node in arch.xpath(
                "//field[@name='lastFiscalNumber']|//field[@name='status_FE']"
            ):
                node.attrib["column_invisible"] = "1"

        return arch, view

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type="form", **options):
        key = super()._get_view_cache_key(view_id, view_type, **options)
        if view_type != "tree":
            return key

        return key + (self.env.company.id,)
