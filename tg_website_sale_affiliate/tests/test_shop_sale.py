from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class WebsiteShopSaleAffiliate(HttpCase):
    def test_auto_apply_discount(self):
        public_category = self.env["product.public.category"].create(
            {"name": "Public Category"}
        )

        self.env["product.product"].create(
            {
                "name": "Small Cabinet",
                "list_price": 100,
                "type": "consu",
                "is_published": True,
                "sale_ok": True,
                "public_categ_ids": [(4, public_category.id)],
                "taxes_id": False,
            }
        )

        ten_percent = self.env["product.product"].create(
            {
                "name": "10.0% discount on total amount",
                "type": "service",
                "supplier_taxes_id": False,
                "sale_ok": False,
                "purchase_ok": False,
                "invoice_policy": "order",
                "default_code": "10PERCENTDISC",
                "categ_id": self.env.ref("product.product_category_all").id,
                "taxes_id": False,
            }
        )

        self.env["loyalty.program"].search([]).write({"active": False})

        program = self.env["loyalty.program"].create(
            {
                "name": "Code for 10% on orders",
                "program_type": "promo_code",
                "trigger": "with_code",
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "mode": "with_code",
                            "code": "testcode",
                        },
                    )
                ],
                "reward_ids": [
                    (
                        0,
                        0,
                        {
                            "reward_type": "discount",
                            "discount": 10,
                            "discount_mode": "percent",
                            "discount_applicability": "order",
                            "discount_line_product_id": ten_percent.id,
                        },
                    )
                ],
            }
        )

        affiliate = self.env["sale.affiliate"].create(
            {
                "name": "Affiliate Test",
                "partner_id": self.env.ref("base.user_admin").partner_id.id,
                "company_id": self.env.company.id,
                "promo_code": "test_affiliate_promo_code",
                "code_promo_program_id": program.id,
            }
        )

        self.start_tour(
            f"/shop?aff_ref={affiliate.id}",
            "tg_auto_set_discount_by_affiliate",
            login="portal",
        )
