from odoo.addons.base.tests.common import HttpCaseWithUserDemo


class TGSaleLoyaltyCommon(HttpCaseWithUserDemo):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if cls.env["ir.module.module"]._get("payment_custom").state != "installed":
            cls.skipTest(cls, reason="Transfer provider is not installed")

        cls.partner_panama = cls.env["res.partner"].create(
            {
                "name": "Noa Noa",
                "email": "noa@example.com",
                "nationality_id": cls.env.ref("base.pa").id,
                "country_id": cls.env.ref("base.pa").id,
                "street": "Streeet",
                "city": "Panama",
                "zip": "0801",
                "phone": "+5072215502",
            }
        )

        public_category = cls.env["product.public.category"].create(
            {"name": "Public Category"}
        )

        cls.env["product.product"].create(
            {
                "name": "Small Cabinet",
                "list_price": 100.0,
                "type": "consu",
                "is_published": True,
                "sale_ok": True,
                "public_categ_ids": [(4, public_category.id)],
                "taxes_id": False,
            }
        )

        cls.user_panama = cls.env["res.users"].create(
            {
                "login": "panama",
                "password": "panama",
                "partner_id": cls.partner_panama.id,
                "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
            }
        )

        cls.partner_demo.nationality_id = cls.env.ref("base.us")

        cls.p1 = cls.env["loyalty.program"].create(
            {
                "name": "Code for 10% on orders",
                "trigger": "with_code",
                "program_type": "promo_code",
                "applies_on": "current",
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "mode": "with_code",
                            "code": "test_10pc",
                        },
                    )
                ],
                "reward_ids": [
                    (
                        0,
                        0,
                        {
                            "reward_type": "discount",
                            "discount_mode": "percent",
                            "discount": 10,
                            "discount_applicability": "order",
                            "required_points": 1,
                        },
                    )
                ],
            }
        )

        cls.ndp = cls.env["nationality.discount.program"].create(
            {
                "nationality": cls.env.ref("base.pa").id,
                "discount_program": cls.p1.id,
            }
        )

        transfer_provider = cls.env.ref("payment.payment_provider_transfer")
        transfer_provider.write(
            {
                "state": "enabled",
                "is_published": True,
            }
        )
        transfer_provider._transfer_ensure_pending_msg_is_set()

        #  Ensure the use of USD (company currency)
        cls.env["product.pricelist"].create({"name": "Public Pricelist"})
