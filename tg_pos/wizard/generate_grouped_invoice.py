from odoo import _, fields, models
from odoo.exceptions import UserError


class GenerateGroupedInvoice(models.TransientModel):
    _name = "generate.grouped.invoice"
    _descrition = "Generate Grouped Invoice Wizard"

    pos_configs = fields.Many2many(
        "pos.config",
        required=True,
        default=lambda self: self._default_pos_configs(),
        context={"active_test": False},
    )
    date_start = fields.Date()
    date_end = fields.Date()

    def _default_pos_configs(self):
        return self.env.context.get("active_ids")

    def generate(self):
        self.ensure_one()

        if not self.date_start:
            raise UserError(_("Start date is not set"))

        if not self.date_end:
            raise UserError(_("End date is not set"))

        sessions = self.env["pos.session"].search(
            [
                ("start_at", ">=", self.date_start),
                ("start_at", "<=", self.date_end),
                ("config_id", "in", self.pos_configs.ids),
            ]
        )
        return sessions._generate_grouped_pos_invoice(self.date_end)
