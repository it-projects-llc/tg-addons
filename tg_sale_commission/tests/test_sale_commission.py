from odoo.addons.sale_commission.tests.test_sale_commission import TestSaleCommission as Base


class TestSaleCommission(Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        company_partner = cls.env["res.partner"].create({
            "name": "Commission Settlement Company",
            "company_type": "company",
        })
        cls.company2 = cls.env["res.company"].create({
            "partner_id": company_partner.id,
            "name": "Company2",
            "currency_id": cls.company.currency_id.id,
        })
        for agent in (
                cls.agent_monthly,
                cls.agent_monthly_paid,
                cls.agent_biweekly,
                cls.agent_quaterly,
                cls.agent_semi,
                cls.agent_annual,
                cls.env.ref("sale_commission.res_partner_pritesh_sale_agent"),
        ):
            cls.env["sale.affiliate"].create({
                "name": agent.name,
                "partner_id": agent.id,
                "company_id": cls.company.id,
            })
        #cls.company.commission_settlement_company = cls.company2

    def _create_sale_order(self, agent, commission):
        # не используй родительский. Сразу создавай как надо
        # TODO:
        if (agent, commission) == (self.agent_semi, self.commission_section_invoice):
            import wdb; wdb.set_trace()
        record = super(TestSaleCommission, self)._create_sale_order(agent, commission)
        affiliate = self.env["sale.affiliate"].search([("partner_id", "=", agent.id)])
        agent.commission_id = commission
        self.assertTrue(affiliate)
        record.affiliate_request_id = self.env["sale.affiliate.request"].create({
            "name": "test",
            "affiliate_id": affiliate.id,
            "ip": "127.0.0.1",
            "referrer": "",
            "user_agent": "IE",
            "accept_language": "",
        })
        return record

    def test_commission_propagation(self):
        # propagation feature is disabled
        pass
