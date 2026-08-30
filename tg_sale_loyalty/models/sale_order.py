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

        all_programs_applied = (
            self.order_line.filtered("is_reward_line").mapped("reward_id.program_id")
            | self._get_points_programs()
        )

        if not program.is_accumulative and all_programs_applied.filtered(
            lambda x: x.trigger == program.trigger
        ):
            return {
                "error": _(
                    "The given code cannot be accumulated with already applied "
                    "discount programs"
                )
            }

        if program.is_accumulative and all_programs_applied.filtered(
            lambda x: not x.is_accumulative
        ).filtered(lambda x: x.trigger == program.trigger):
            return {
                "error": _("There is already non-accumulative discount program applied")
            }

        return super()._try_apply_code(code)
