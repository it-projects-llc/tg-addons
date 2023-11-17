from urllib.parse import urljoin

from odoo import fields, models


class SaleAffiliate(models.Model):
    _inherit = ["sale.affiliate", "mail.thread"]
    _name = "sale.affiliate"

    active = fields.Boolean(default=True)

    valid_hours = fields.Integer(default=-1)
    valid_sales = fields.Integer(default=-1)

    partner_id = fields.Many2one("res.partner")
    code_promo_program_id = fields.Many2one(
        "coupon.program",
        string="Promo Program",
        context="{'form_view_ref': 'coupon.coupon_program_view_promo_program_form', 'lock_promo_code_usage': 1, 'default_program_type': 'promotion_program', 'default_promo_code_usage': 'code_needed', 'default_company_id': company_id}",  # noqa: E950
        domain="[('program_type', '=', 'promotion_program'), ('promo_code_usage', '=', 'code_needed'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",  # noqa: E950
        copy=False,
    )
    order_count = fields.Integer(compute="_compute_order_count")
    invoice_count = fields.Integer(compute="_compute_invoice_count")
    referal_link = fields.Char(compute="_compute_referal_link")

    _sql_constraints = [
        (
            "partner_id_unique",
            "unique(partner_id, company_id)",
            "Partner must be unique",
        ),
        ("name_unique", "unique(name)", "Affiliate name must be unique"),
    ]

    def _get_order_dict(self):
        self.env.cr.execute(
            """
SELECT sar.affiliate_id, array_agg(DISTINCT so.id)
FROM sale_affiliate_request sar
LEFT JOIN sale_order so ON so.affiliate_request_id = sar.id
WHERE so.id IS NOT NULL AND sar.affiliate_id IN %s
GROUP BY sar.affiliate_id
        """,
            [tuple(self.ids)],
        )

        return {row[0]: row[1] for row in self.env.cr.fetchall()}

    def _get_invoice_dict(self):
        self.env.cr.execute(
            """
SELECT sar.affiliate_id, array_agg(DISTINCT aml.move_id)
FROM sale_affiliate_request sar
LEFT JOIN sale_order so ON so.affiliate_request_id = sar.id
LEFT JOIN sale_order_line sol ON sol.order_id = so.id
LEFT JOIN sale_order_line_invoice_rel solir ON solir.order_line_id = sol.id
LEFT JOIN account_move_line aml ON aml.id = solir.invoice_line_id
WHERE aml.move_id IS NOT NULL AND sar.affiliate_id IN %s
GROUP BY sar.affiliate_id
        """,
            [tuple(self.ids)],
        )

        return {row[0]: row[1] for row in self.env.cr.fetchall()}

    def _compute_order_count(self):
        r = self._get_order_dict()

        for record in self:
            record.order_count = len(r.get(record.id, []))

    def _compute_invoice_count(self):
        r = self._get_invoice_dict()

        for record in self:
            record.invoice_count = len(r.get(record.id, []))

    def _compute_referal_link(self):
        for record in self:
            if record.company_id.website:
                base_url = record.company_id.website
            else:
                base_url = record.get_base_url()
            record.referal_link = urljoin(base_url, f"/events?aff_ref={record.id}")

    def action_show_orders(self):
        order_dict = self._get_order_dict()
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        action["domain"] = [("id", "in", order_dict.get(self.id) or [])]
        action["context"] = {
            "create": False,
        }
        return action

    def action_show_invoices(self):
        invoice_dict = self._get_invoice_dict()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_out_invoice_type"
        )
        action["domain"] = [("id", "in", invoice_dict.get(self.id) or [])]
        action["context"] = {
            "create": False,
        }
        return action

    def _send_invitation(self):
        self.ensure_one()
        self.env.context.get("lang")
        template = self.env.ref(
            "tg_website_sale_affiliate.send_invitation_mail_template"
        )
        if template.lang:
            template._render_lang(self.ids)[self.id]
        ctx = {
            "default_model": self._name,
            "default_res_id": self.ids[0],
            "default_use_template": True,
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "force_email": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }
