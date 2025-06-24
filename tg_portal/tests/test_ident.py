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

    # Case: if not partner.has_cedula
    def test_inverse_has_cedula_clears_field(self):
        partner = self.env["res.partner"].create(
            {"name": "Partner with cedula", "cedula": "cedula 1"}
        )
        self.assertTrue(partner.has_cedula)
        partner.has_cedula = False
        partner._inverse_has_cedula()
        self.assertFalse(partner.cedula)

    def test_inverse_identification2_behaviors(self):
        category = self.env["res.partner.id_category"].create(
            {"code": "passport", "name": "Passport"}
        )
        partner = self.env["res.partner"].create({"name": "Partner with one ID"})

        # Case: only 1 ID exists and new value is provided - update name
        id1 = self.env["res.partner.id_number"].create(
            {"partner_id": partner.id, "category_id": category.id, "name": "OLD"}
        )
        partner.passport = "UPDATED"
        partner._inverse_identification2("passport", "passport")
        id1.invalidate_cache()
        self.assertEqual(id1.name, "UPDATED")

        # Case: only 1 ID exists and value is empty - active = False
        partner.passport = ""
        partner._inverse_identification2("passport", "passport")
        id1.invalidate_cache()
        self.assertFalse(id1.active)

        # Case: multiple ID numbers and empty name — should skip
        self.env["res.partner.id_number"].create(
            {"partner_id": partner.id, "category_id": category.id, "name": "SECOND"}
        )
        count_before = len(partner.id_numbers)
        partner.passport = ""
        partner._inverse_identification2("passport", "passport")
        self.assertEqual(len(partner.id_numbers), count_before)

        # Case: partner has multiple id_numbers — new ID is added with the given value
        partner.passport = "NEW_ENTRY"
        partner._inverse_identification2("passport", "passport")
        self.assertIn("NEW_ENTRY", partner.id_numbers.mapped("name"))
