from odoo import models


class Website(models.Model):
    _inherit = "website"

    def sale_get_order(self, *args, **kw):
        order = super().sale_get_order(*args, **kw)

        customer_nationality = order.partner_id.nationality_id
        if customer_nationality:
            ndp = (
                self.env["nationality.discount.program"]
                .search(
                    [
                        ("nationality", "=", customer_nationality.id),
                        ("company_id", "=", order.company_id.id),
                    ],
                    limit=1,
                )
                .sudo()
            )
            if ndp.discount_code:
                order._try_apply_code(ndp.discount_code)

        return order
