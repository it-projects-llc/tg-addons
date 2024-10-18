from odoo import api, fields, models


class PartnerMarketingAnswer(models.Model):
    _name = "res.partner.marketing.answer"
    _description = "Marketing answers"
    _order = "sequence, id"
    _rec_name = "answer"

    sequence = fields.Integer(default=10)
    field = fields.Many2one(
        "ir.model.fields",
        domain="[('model', '=', 'res.partner'), ('name', 'like', 'marketing_')]",
        required=True,
        ondelete="cascade",
    )
    answer = fields.Char(
        required=True,
    )
    is_canned = fields.Boolean()

    @api.model
    def _create_custom_answer(self, field_name, answer):
        assert field_name.startswith("marketing_")
        field = self.field.search(
            [("name", "=", field_name), ("model", "=", "res.partner")]
        )
        return self.create({"field": field.id, "answer": answer, "is_canned": False})
