from odoo import api, fields, models
from odoo.tools import defaultdict
from urllib.parse import urljoin


class SaleAffiliate(models.Model):
    _inherit = ["sale.affiliate", "mail.thread"]
    _name = "sale.affiliate"

    valid_hours = fields.Integer(default=-1)
    valid_sales = fields.Integer(default=-1)

    partner_id = fields.Many2one("res.partner")
    code_promo_program_id = fields.Many2one(
        'coupon.program',
        string="Promo Program",
        domain="[('promo_code_usage', '=', 'code_needed'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        copy=False,
    )
    order_count = fields.Integer(compute="_compute_order_count")
    referal_link = fields.Char(compute="_compute_referal_link")

    def _get_order_dict(self):
        self.env.cr.execute("""
SELECT sar.affiliate_id, array_agg(so.id)
FROM sale_affiliate_request sar
LEFT JOIN sale_order so ON so.affiliate_request_id = sar.id
WHERE sar.affiliate_id IN %s
GROUP BY sar.affiliate_id
        """, [tuple(self.ids)])

        return dict((row[0], row[1]) for row in self.env.cr.fetchall())

    def _compute_order_count(self):
        r = self._get_order_dict()

        for record in self:
            record.order_count = len(r.get(record.id, []))

    def _compute_referal_link(self):
        for record in self:
            record.referal_link = urljoin(record.get_base_url(), f"/events?aff_ref={record.id}")

    def action_show_orders(self):
        order_dict = self._get_order_dict()
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        action['domain'] = [('id', 'in', order_dict.get(self.id) or [])]
        action['context'] = {
            'create': False,
            'edit': False,
        }
        return action

    def _subscribe_partner(self):
        for record in self:
            record.message_subscribe(partner_ids=record.partner_id.ids)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(SaleAffiliate, self).create(vals_list)
        records._subscribe_partner()
        return records

    def write(self, vals):
        res = super(SaleAffiliate, self).write(vals)
        self._subscribe_partner()
        return res
