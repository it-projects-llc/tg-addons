from odoo import api, fields, models
from odoo.tools import defaultdict
from urllib.parse import urljoin


class SaleAffiliate(models.Model):
    _inherit = "sale.affiliate"

    partner_id = fields.Many2one("res.partner")
    code_promo_program_id = fields.Many2one(
        'coupon.program',
        string="Promo Program",
        domain="[('promo_code_usage', '=', 'code_needed'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        copy=False,
    )
    order_count = fields.Integer(compute="_compute_order_count")
    referal_link = fields.Char(compute="_compute_referal_link")

    def _compute_order_count(self):
        self.env.cr.execute("""
SELECT sar.affiliate_id, COUNT(so.id)
FROM sale_affiliate_request sar
LEFT JOIN sale_order so ON so.affiliate_request_id = sar.id
WHERE sar.affiliate_id IN %s
GROUP BY sar.affiliate_id
        """, [tuple(self.ids)])

        r = dict((row[0], row[1]) for row in self.env.cr.fetchall())
        for record in self:
            record.order_count = r.get(record.id, 0)

    def _compute_referal_link(self):
        for record in self:
            record.referal_link = urljoin(record.get_base_url(), f"/events?aff_ref={record.id}")
