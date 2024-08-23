from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    marketing_answers = fields.Many2many(
        "event.registration.answer", compute="_compute_marketing_answers"
    )

    def _compute_marketing_answers(self):
        all_marketing_anwsers = self.env["event.registration.answer"].search(
            [
                ("registration_id.partner_id", "in", self.ids),
            ]
        )
        for partner in self:
            partner.marketing_answers = all_marketing_anwsers.filtered(
                lambda x: x.registration_id.partner_id == partner
            )
