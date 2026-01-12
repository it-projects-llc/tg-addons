from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    accomodation_category = fields.Many2one(
        "product.public.category",
        compute="_compute_accomodation_category",
        compute_sudo=True,
    )

    def _compute_accomodation_category(self):
        get_param = self.env["ir.config_parameter"].get_param
        accomodation_category_id = int(get_param("tg.accomodation_category", 0))
        if not accomodation_category_id:
            accomodation_category_id = False

        for record in self:
            record.accomodation_category = accomodation_category_id
