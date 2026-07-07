from odoo import fields, models


class NationalityDiscountProgram(models.Model):
    _name = "nationality.discount.program"
    _description = "Nationality discount program"

    nationality = fields.Many2one("res.country", required=True)
    discount_program = fields.Many2one("loyalty.program", required=True)
    company_id = fields.Many2one(
        "res.company", related="discount_program.company_id", store=True
    )
