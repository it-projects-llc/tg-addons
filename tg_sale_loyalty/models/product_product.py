from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def action_show_loyalty_programs(self):
        return self.product_tmpl_id.action_show_loyalty_programs()
