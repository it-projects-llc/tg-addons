from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    related_loyalty_programs = fields.Many2many(
        "loyalty.program", compute="_compute_related_loyalty_programs"
    )
    has_related_loyalty_programs = fields.Boolean(
        compute="_compute_related_loyalty_programs"
    )

    def _compute_related_loyalty_programs(self):
        rewards = self.env["loyalty.reward"].search(
            [
                (
                    "discount_line_product_id",
                    "in",
                    self.mapped("product_variant_ids").ids,
                ),
            ]
        )
        rewards.mapped("discount_line_product_id.product_tmpl_id")

        for record in self:
            related_rewards = rewards.filtered(
                lambda x, record=record: x.discount_line_product_id.product_tmpl_id
                & record
            )
            record.related_loyalty_programs = related_rewards.mapped("program_id")
            record.has_related_loyalty_programs = bool(record.related_loyalty_programs)

    def action_show_loyalty_programs(self):
        self.ensure_one()

        programs = self.related_loyalty_programs
        if not programs:
            return {"type": "ir.actions.act_window_close"}

        action = self.env["ir.actions.act_window"]._for_xml_id(
            "loyalty.loyalty_program_discount_loyalty_action"
        )
        if len(programs) > 1:
            action["domain"] = [("id", "in", programs.ids)]
        elif len(programs) == 1:
            action.update(views=[(False, "form")], res_id=programs.id)

        return action
