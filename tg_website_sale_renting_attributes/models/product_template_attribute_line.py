from odoo import api, fields, models


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    attribute_domain = fields.Binary(compute="_compute_attribute_domain")

    @api.depends("product_tmpl_id.rent_via_period_ok")
    def _compute_attribute_domain(self):
        for record in self:
            if record.product_tmpl_id.rent_via_period_ok:
                record.attribute_domain = []
            else:
                record.attribute_domain = [("is_period", "=", False)]

    def action_open_attribute_values(self):
        res = super().action_open_attribute_values()
        if self.attribute_id.is_period:
            res["context"].update(show_period_start_end=True)
        return res
