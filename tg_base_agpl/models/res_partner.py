from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    passport = fields.Char(
        string="Passport Number",
        compute=lambda s: s._compute_identification(
            "passport",
            "passport",
        ),
        inverse=lambda s: s._inverse_identification(
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
        inverse=lambda s: s._inverse_identification(
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
