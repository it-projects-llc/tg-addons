from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_loyalty_program(self):
        res = super()._loader_params_loyalty_program()
        res["search_params"]["fields"] += [
            "happy_hours_weekdays",
            "are_happy_hours_enabled",
        ]
        return res
