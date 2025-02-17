from odoo.tests.common import TransactionCase


class TestPartnerIdentificationBase(TransactionCase):
    def _test_multiple_idents(self, ident_code):
        partner = self.env["res.partner"].create(
            {
                "name": "Partner with multiple idents",
            }
        )

        partner[ident_code] = "123"  # this creates ident category record
        ident_category = self.env["res.partner.id_category"].search(
            [
                ("code", "=", ident_code),
            ]
        )
        self.assertTrue(bool(ident_category))

        partner.write(
            {
                "name": "Partner with multiple idents",
                "id_numbers": [
                    (
                        0,
                        0,
                        {
                            "name": "456",
                            "category_id": ident_category.id,
                        },
                    )
                ],
            }
        )
        self.assertEqual(len(partner.id_numbers), 2)

        new_ident_code = "345"
        partner[ident_code] = new_ident_code
        self.assertEqual(len(partner.id_numbers), 3)

        # this also ensures, that last updated one is used as current
        first_by_name = sorted(partner.mapped("id_numbers.name"))[0]
        self.assertNotEqual(first_by_name, new_ident_code, "Incorrect test case")

        partner.invalidate_recordset()
        self.assertEqual(partner[ident_code], new_ident_code)

    def test_multiple_passport(self):
        self._test_multiple_idents("passport")

    def test_multiple_cedula(self):
        self._test_multiple_idents("cedula")
