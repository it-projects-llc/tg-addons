from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_loyalty_program(self):
        res = super()._loader_params_loyalty_program()
        res["search_params"]["fields"] += [
            "are_happy_hours_enabled",
            "happy_hours_from",
            "happy_hours_to",
        ]
        return res

    def _pos_data_process(self, loaded_data):
        Programs = self.env["loyalty.program"]
        res = super()._pos_data_process(loaded_data)

        for p in loaded_data.get("loyalty.program", []):
            if not p["are_happy_hours_enabled"]:
                continue

            program = Programs.browse(p["id"])
            p["happy_hours_weekdays"] = []
            for i, weekday in enumerate(
                (
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                ),
                start=1,
            ):
                if program["happy_hours_" + weekday]:
                    p["happy_hours_weekdays"].append(i)

        return res
