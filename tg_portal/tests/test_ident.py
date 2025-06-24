from odoo.tests.common import TransactionCase


class TestPartnerIdentificationBase(TransactionCase):
    def _test_multiple_idents(self, ident_code):
        partner = self.env["res.partner"].create(
            {"name": "Partner with multiple idents"}
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
<<<<<<< HEAD
        self.assertFalse(partner.cedula)

    def test_passport_deactivation(self):
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        partner.passport = "OLD"
        passport = self.env["res.partner.id_number"].search(
            [
                ("partner_id", "=", partner.id),
                ("category_id.code", "=", "passport"),
            ]
        )
        self.assertTrue(passport)
        self.assertTrue(passport.active)
        partner.passport = ""
        self.assertFalse(passport.active)

    def test_cedula_update_behavior(self):
        partner = self.env["res.partner"].create({"name": "Partner Cedula test"})

        # Only one cedula – should update
        partner.cedula = "CEDULA_OLD"
        cedulas = partner.id_numbers.filtered(lambda r: r.category_id.code == "cedula")
        self.assertEqual(len(cedulas), 1)
        self.assertEqual(cedulas[0].name, "CEDULA_OLD")

        partner.cedula = "CEDULA_UPDATED"
        cedulas = partner.id_numbers.filtered(lambda r: r.category_id.code == "cedula")
        self.assertEqual(len(cedulas), 1)
        self.assertEqual(cedulas[0].name, "CEDULA_UPDATED")

        cedula_category = partner.id_numbers.filtered(
            lambda r: r.category_id.code == "cedula"
        ).mapped("category_id")[0]

        # Multiple cedulas – should create new
        self.env["res.partner.id_number"].create(
            {
                "partner_id": partner.id,
                "category_id": cedula_category.id,
                "name": "CEDULA_2",
            }
        )
        self.env["res.partner.id_number"].create(
            {
                "partner_id": partner.id,
                "category_id": cedula_category.id,
                "name": "CEDULA_3",
            }
        )
        self.assertEqual(
            len(
                partner.id_numbers.filtered(lambda r: r.category_id == cedula_category)
            ),
            3,
        )

        partner.cedula = "NEW_CEDULA"
        cedulas = partner.id_numbers.filtered(
            lambda r: r.category_id == cedula_category
        )
        self.assertEqual(len(cedulas), 4)
        self.assertIn("NEW_CEDULA", cedulas.mapped("name"))
        self.assertEqual(partner.cedula, "NEW_CEDULA")
