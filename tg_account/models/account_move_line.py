from collections import defaultdict

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def copy_data(self, default=None):
        data_list = super().copy_data(default)

        if not self.env.context.get("duplicate_invoice_to_fiscal_company"):
            return data_list

        fiscal_company_id = self.env.context.get("duplicate_invoice_to_fiscal_company")
        AccountMappings = self.sudo().env["res.company.fiscal.mapping.account"]
        TaxMappings = self.sudo().env["res.company.fiscal.mapping.tax"]

        accounts_to_search = defaultdict(set)
        taxes_to_search = defaultdict(set)
        for line in self:
            accounts_to_search[line.company_id.id].add(line.account_id.id)
            for tax in line.tax_ids:
                taxes_to_search[line.company_id.id].add(tax.id)

        accounts_mapping = {}
        for company_from, accounts_from in accounts_to_search.items():
            mappings = AccountMappings.search(
                [
                    ("company_from", "=", company_from),
                    ("company_to", "=", fiscal_company_id),
                    ("account_from", "in", list(accounts_from)),
                ]
            )
            for mapping in mappings:
                accounts_mapping[
                    (mapping.company_from.id, mapping.account_from.id)
                ] = mapping.account_to.id

        taxes_mapping = {}
        for company_from, taxes_from in taxes_to_search.items():
            mappings = TaxMappings.search(
                [
                    ("company_from", "=", company_from),
                    ("company_to", "=", fiscal_company_id),
                    ("tax_from", "in", list(taxes_from)),
                ]
            )
            for mapping in mappings:
                taxes_mapping[
                    (mapping.company_from.id, mapping.tax_from.id)
                ] = mapping.tax_to.id

        for line, data in zip(self, data_list, strict=False):
            company_id = line.company_id.id
            new_account_id = accounts_mapping.get((company_id, line.account_id.id))

            if new_account_id:
                data["account_id"] = new_account_id

            if "tax_ids" in data:
                new_tax_ids = []
                for triplet in data["tax_ids"]:
                    if triplet[0] == 6:
                        triplet = triplet[:2] + (
                            [taxes_mapping.get((company_id, x), x) for x in triplet[2]],
                        )

                    new_tax_ids.append(triplet)

                data["tax_ids"] = new_tax_ids

            # TODO: Надо у Ноа спросить, можно ли так?
            data["tax_repartition_line_id"] = False

        return data_list
