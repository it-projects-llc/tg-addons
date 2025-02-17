from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    is_passport_not_ready = fields.Boolean()

    passport = fields.Char(
        string="Passport Number",
        compute=lambda s: s._compute_identification(
            "passport",
            "passport",
        ),
        inverse=lambda s: s._inverse_identification2(
            "passport",
            "passport",
        ),
        search=lambda s, *a: s._search_identification("passport", *a),
    )

    cedula = fields.Char(
        string="Cedula Number",
        compute=lambda s: s._compute_identification(
            "cedula",
            "cedula",
        ),
        inverse=lambda s: s._inverse_identification2(
            "cedula",
            "cedula",
        ),
        search=lambda s, *a: s._search_identification("cedula", *a),
    )
    has_cedula = fields.Boolean(
        compute="_compute_has_cedula",
        inverse="_inverse_has_cedula",
        store=True,
    )

    @api.depends("cedula")
    def _compute_has_cedula(self):
        for partner in self:
            partner.has_cedula = bool(partner.cedula)

    def _inverse_has_cedula(self):
        for partner in self:
            if not partner.has_cedula:
                partner.cedula = ""

    # based on _inverse_identification from partner_identification
    # ValidationError was removed for multiple IDs case
    def _inverse_identification2(self, field_name, category_code):
        for record in self:
            id_number = record.id_numbers.filtered(
                lambda r: r.category_id.code == category_code
            )
            record_len = len(id_number)

            if record_len == 1:
                value = record[field_name]
                if value:
                    id_number.name = value
                else:
                    id_number.active = False
            else:
                name = record[field_name]
                if not name:
                    # No value to set
                    continue
                category = self.env["res.partner.id_category"].search(
                    [("code", "=", category_code)]
                )
                if not category:
                    category = self.env["res.partner.id_category"].create(
                        {"code": category_code, "name": category_code}
                    )
                self.env["res.partner.id_number"].create(
                    {"partner_id": record.id, "category_id": category.id, "name": name}
                )


class PartnerIdNumber(models.Model):
    _inherit = "res.partner.id_number"
    _order = "write_date DESC, id DESC"
