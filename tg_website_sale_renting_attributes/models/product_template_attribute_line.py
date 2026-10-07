from odoo import api, fields, models


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    attribute_domain = fields.Binary(compute="_compute_attribute_domain")

    @api.depends("product_tmpl_id.rent_via_period_ok")
    def _compute_attribute_domain(self):
        for record in self:
            if record.product_tmpl_id.rent_via_period_ok:
                record.attribute_domain = [("is_period", "=", True)]
            else:
                record.attribute_domain = []
