def post_load():
    from odoo.addons.point_of_sale.models.pos_config import OR, PosConfig

    def _get_available_product_domain(self):
        domain = [
            *self.env["product.product"]._check_company_domain(self.company_id),
            ("available_in_pos", "=", True),
            ("sale_ok", "=", True),
        ]
        if self.limit_categories and self.iface_available_categ_ids:
            domain.append(("pos_categ_ids", "in", self.iface_available_categ_ids.ids))
        # changes start
        if self.shop_ref_id:
            domain.append(("shop_ids", "in", self.shop_ref_id.ids))
        # changes end
        if self.iface_tipproduct:
            domain = OR([domain, [("id", "=", self.tip_product_id.id)]])
        return domain

    PosConfig._get_available_product_domain = _get_available_product_domain
