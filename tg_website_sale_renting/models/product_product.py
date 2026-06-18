from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def _website_show_quick_add(self):
        self.ensure_one()
        if self.rend_ok:
            # escaping situation when mixing product
            # with different allowed renting periods
            return False

        return super()._website_show_quick_add()
