from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_program_domain(self):
        res = super()._get_program_domain()
        res += [
            "|",
            ("nationality_programs", "=", False),
            (
                "nationality_programs.nationality",
                "=",
                self.partner_id.nationality_id.id,
            ),
        ]
        return res
