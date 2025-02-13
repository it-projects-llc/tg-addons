from odoo import _, models
from odoo.osv import expression


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _try_apply_code(self, code):
        if isinstance(code, str):
            code = code.strip()

        # almost copy-paste from sale_loyalty from _try_apply_code
        base_domain = self._get_trigger_domain()
        domain = expression.AND(
            [base_domain, [("mode", "=", "with_code"), ("code", "=", code)]]
        )
        rule = self.env["loyalty.rule"].search(domain)
        program = rule.program_id
        coupon = False

        if rule in self.code_enabled_rule_ids:
            # it will fail in sale_loyalty
            return super()._try_apply_code(code)

        if not program:
            coupon = self.env["loyalty.card"].search([("code", "=", code)])
            program = coupon.program_id

        if not program or not program.active:
            return super()._try_apply_code(code)

        # almost copy-pase from sale_loyalty from _try_apply_code stops here

        points_programs = self._get_points_programs()
        coupon_programs = self.applied_coupon_ids.program_id
        program_domain = self._get_program_domain()
        domain = expression.AND(
            [
                program_domain,
                [
                    ("id", "not in", points_programs.ids),
                    ("trigger", "=", "auto"),
                    ("rule_ids.mode", "=", "auto"),
                ],
            ]
        )
        automatic_programs = (
            self.env["loyalty.program"]
            .search(domain)
            .filtered(lambda p: not p.limit_usage or p.total_order_count < p.max_usage)
        )

        all_programs_applied = points_programs | coupon_programs | automatic_programs

        if not program.is_accumulative and all_programs_applied:
            return {
                "error": _(
                    "Given code cannot be accumulated with already applied programs"
                )
            }

        if program.is_accumulative and all_programs_applied.filtered(
            lambda x: not x.is_accumulative
        ):
            return {
                "error": _("There is already applied non-accumulative program applied")
            }

        return super()._try_apply_code(code)
