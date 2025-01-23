from urllib.parse import urljoin

from odoo import fields, models


class SaleAffiliate(models.Model):
    _inherit = "sale.affiliate"

    referal_link = fields.Char(compute="_compute_referal_link")
    portal_link = fields.Char(compute="_compute_referal_link")

    def _compute_referal_link(self):
        for record in self:
            if record.company_id.website:
                base_url = record.company_id.website
            else:
                base_url = record.get_base_url()
            record.referal_link = urljoin(base_url, f"/events?aff_ref={record.id}")
            record.portal_link = urljoin(record.get_base_url(), "/my/affiliates")
