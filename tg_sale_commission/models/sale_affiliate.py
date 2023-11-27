from odoo import fields, models


class SaleAffiliate(models.Model):
    _inherit = "sale.affiliate"

    partner_id = fields.Many2one("res.partner", domain="[('agent', '=', True)]")
    bill_count = fields.Integer(compute="_compute_bill_count")
    commission_id = fields.Many2one(
        "sale.commission",
        related="partner_id.commission_id",
        store=False,
        readonly=False,
    )

    def _get_bill_dict(self):
        self.env.cr.execute(
            """
SELECT partner_id, array_agg(id)
FROM account_move
WHERE id IN (
    SELECT move_id
    FROM account_move_line
    WHERE settlement_id IN (
        SELECT id
        FROM sale_commission_settlement
        WHERE agent_id IN %s
    )
)
GROUP BY partner_id
        """,
            [tuple(self.mapped("partner_id").ids)],
        )

        return {row[0]: row[1] for row in self.env.cr.fetchall()}

    def _compute_bill_count(self):
        r = self._get_bill_dict()

        for record in self:
            record.bill_count = len(r.get(record.partner_id.id, []))

    def action_show_bills(self):
        bill_dict = self._get_bill_dict()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_in_invoice_type"
        )
        action["domain"] = [("id", "in", bill_dict.get(self.partner_id.id) or [])]
        action["context"] = {
            "default_move_type": "in_invoice",
            "create": False,
        }
        return action
