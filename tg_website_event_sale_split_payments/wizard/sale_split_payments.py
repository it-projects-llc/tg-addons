from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleSplitPayments(models.TransientModel):
    _name = "sale.split.payments"
    _description = "Splt Payments Wizard"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get("active_id")
        if not active_id:
            return res

        res["so"] = active_id

        so = self.env["sale.order"].browse(active_id)
        if so.state != "draft":
            raise UserError(_("Split payments can be applied only to draft orders"))

        min_deposit, max_deposit = so._calculate_min_max_deposit()
        res["min_deposit"] = min_deposit
        res["max_deposit"] = max_deposit
        res["deposit"] = min_deposit

        return res

    min_deposit = fields.Monetary(readonly=True)
    max_deposit = fields.Monetary(readonly=True)

    so = fields.Many2one("sale.order", required=True, readonly=True)
    currency_id = fields.Many2one(related="so.currency_id")
    deposit = fields.Monetary()
    payment_count = fields.Integer(default=2)
    period = fields.Selection(
        [
            ("month", "Monthly"),
            ("biweekly", "Biweekly"),
        ],
        default="month",
    )

    def action_split(self):
        self.ensure_one()

        deposit = self.deposit
        payment_count = self.payment_count
        period = self.period

        self.so._generate_invoice_plan_for_event(deposit, payment_count, period)
