from odoo import fields, models


class PartnerMarketingAnswer(models.Model):
    _name = "res.partner.marketing.answer"
    _description = "Marketing answers"
    _order = "sequence ASC, id ASC"
    _rec_name = "answer"

    sequence = fields.Integer(default=10)
    field = fields.Many2one(
        "ir.model.fields",
        domain="[('model', '=', 'res.partner'), ('name', 'like', 'marketing_')]",
    )
    answer = fields.Char()
    is_canned = fields.Boolean()
