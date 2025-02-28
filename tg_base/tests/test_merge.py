from odoo.tests.common import TransactionCase, new_test_user


class TestPartnerMerge(TransactionCase):
    def test_merge_with_users_01(self):
        partner1 = self.env["res.partner"].create({"name": "test partner 1"})
        user1 = new_test_user(self.env, "user1@odoo.com", partner_id=partner1.id)

        partner2 = self.env["res.partner"].create({"name": "test partner 2"})
        user2 = new_test_user(self.env, "user2@odoo.com", partner_id=partner2.id)

        self.env["base.partner.merge.automatic.wizard"]._merge(
            (partner1 + partner2).ids,
            partner1,
        )

        self.assertEqual(user2.partner_id, partner1)
        self.assertFalse(user2.active)
        self.assertEqual(user1.partner_id, partner1)
        self.assertTrue(user1.active)
