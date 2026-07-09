from odoo import api, fields, models


class NationalityDiscountProgram(models.Model):
    _name = "nationality.discount.program"
    _description = "Nationality discount program"

    nationality = fields.Many2one("res.country", required=True)
    discount_program = fields.Many2one(
        "loyalty.program", required=True, domain="[('program_type', '=', 'promo_code')]"
    )
    discount_code = fields.Char(compute="_compute_discount_code")
    company_id = fields.Many2one(
        "res.company", related="discount_program.company_id", store=True
    )

    @api.depends("discount_program.rule_ids.code")
    def _compute_discount_code(self):
        for record in self:
            record.discount_code = record.discount_program.rule_ids[:1].code
