from odoo import _, models


class Website(models.Model):
    _inherit = "website"

    def _get_checkout_steps(self, current_step=None):
        res = super()._get_checkout_steps(current_step=current_step)
        if current_step == "website_sale.checkout":
            order = self.sale_get_order()
            if order and order._should_include_accomodation():
                accomodation_category = order.company_id.accomodation_category
                res.update(
                    main_button=_("Choose accommodation"),
                    main_button_href=f"/shop/category/{accomodation_category.id}",
                )
        return res
