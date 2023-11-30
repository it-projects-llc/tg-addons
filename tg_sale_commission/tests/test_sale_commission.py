from odoo.addons.sale_commission.tests.test_sale_commission import (
    TestSaleCommission as Base,
)

Base.__unittest_skip__ = True  # do not run tests of original sale_commission


class TestSaleCommission(Base):
    __unittest_skip__ = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company_partner = cls.env["res.partner"].create(
            {
                "name": "Commission Settlement Company",
                "company_type": "company",
            }
        )
        cls.company2 = cls.env["res.company"].create(
            {
                "partner_id": company_partner.id,
                "name": "Company2",
                "currency_id": cls.company.currency_id.id,
            }
        )
        for agent in (
            cls.agent_monthly,
            cls.agent_monthly_paid,
            cls.agent_biweekly,
            cls.agent_quaterly,
            cls.agent_semi,
            cls.agent_annual,
            cls.env.ref("sale_commission.res_partner_pritesh_sale_agent"),
        ):
            cls.env["sale.affiliate"].create(
                {
                    "name": agent.name,
                    "partner_id": agent.id,
                    "company_id": cls.company.id,
                }
            )
        cls.company.commission_settlement_company = cls.company2

    def _create_sale_order(self, agent, commission):
        agent.commission_id = commission

        affiliate = self.env["sale.affiliate"].search([("partner_id", "=", agent.id)])
        self.assertTrue(affiliate)

        sale_order = self.sale_order_model.create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "product_uom": self.ref("uom.product_uom_unit"),
                            "price_unit": self.product.lst_price,
                        },
                    )
                ],
            }
        )
        sale_order.affiliate_request_id = self.env["sale.affiliate.request"].create(
            {
                "name": "test",
                "affiliate_id": affiliate.id,
                "ip": "127.0.0.1",
                "referrer": "",
                "user_agent": "IE",
                "accept_language": "",
            }
        )

        return sale_order

    def test_commission_propagation(self):
        # propagation feature is disabled
        pass
