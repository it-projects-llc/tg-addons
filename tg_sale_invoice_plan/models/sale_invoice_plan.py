from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleInvoicePlan(models.Model):
    _name = "sale.invoice.plan"
    _description = "Invoice Planning Detail"
    _order = "installment"

    sale_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sales Order",
        index=True,
        readonly=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        related="sale_id.partner_id",
        store=True,
        index=True,
    )
    state = fields.Selection(
        string="Status",
        related="sale_id.state",
        store=True,
        index=True,
    )
    installment = fields.Integer()
    plan_date = fields.Date(required=True)
    last = fields.Boolean(
        string="Last Installment",
        compute="_compute_last",
        help="Last installment will create invoice use remaining amount",
    )
    amount = fields.Float()
    invoice_move_ids = fields.Many2many(
        "account.move",
        relation="sale_invoice_plan_invoice_rel",
        column1="plan_id",
        column2="move_id",
        string="Invoices",
        readonly=True,
    )
    amount_invoiced = fields.Float(compute="_compute_invoiced", store=True)
    to_invoice = fields.Boolean(
        string="Next Invoice",
        compute="_compute_to_invoice",
        help="If this line is ready to create new invoice",
    )
    invoiced = fields.Boolean(
        string="Invoice Created",
        compute="_compute_invoiced",
        store=True,
        help="If this line already invoiced",
    )
    no_edit = fields.Boolean(
        compute="_compute_no_edit",
    )

    _sql_constraint = [
        (
            "unique_instalment",
            "UNIQUE (sale_id, installment)",
            "Installment must be unique on invoice plan",
        )
    ]

    def _no_edit(self):
        self.ensure_one()
        return self.invoiced

    def _compute_no_edit(self):
        for rec in self:
            rec.no_edit = rec._no_edit()

    def _compute_to_invoice(self):
        """If any invoice is in draft/open/paid do not allow to create inv.
        Only if previous to_invoice is False, it is eligible to_invoice.
        """
        for rec in self:
            rec.to_invoice = False
        for rec in self.sorted("installment"):
            if rec.state != "sale":  # Not confirmed, no to_invoice
                continue
            if not rec.invoiced:
                rec.to_invoice = True
                break

    def _get_amount_invoice(self, invoices):
        """Hook function"""
        amount_invoiced = sum(invoices.mapped("amount_total"))
        deposit_product_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale.default_deposit_product_id")
        )
        if deposit_product_id:
            lines = invoices.mapped("invoice_line_ids").filtered(
                lambda line: line.product_id.id != int(deposit_product_id)
            )
            amount_invoiced = sum(lines.mapped("price_total"))
        return amount_invoiced

    @api.depends("invoice_move_ids.state")
    def _compute_invoiced(self):
        for rec in self:
            invoiced = rec.invoice_move_ids.filtered(
                lambda line: line.state in ("draft", "posted")
            )
            rec.invoiced = True if invoiced else False
            rec.amount_invoiced = rec._get_amount_invoice(invoiced[:1])

    def _compute_last(self):
        for rec in self:
            last = max(rec.sale_id.invoice_plan_ids.mapped("installment"))
            rec.last = rec.installment == last

    def unlink(self):
        lines = self.filtered("no_edit")
        if lines:
            installments = [str(x) for x in lines.mapped("installment")]
            raise UserError(
                _(
                    "Installment %s: already used and not allowed to delete.\n"
                    "Please discard changes."
                )
                % ", ".join(installments)
            )
        return super().unlink()
