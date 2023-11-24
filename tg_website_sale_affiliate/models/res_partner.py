from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    affiliates = fields.One2many("sale.affiliate", "partner_id")
    affiliate_count = fields.Integer(compute="_compute_affiliate_count")

    def action_show_affiliates(self):
        affiliates = self.mapped("affiliates")
        action = self.env["ir.actions.actions"]._for_xml_id(
            "website_sale_affiliate.sale_affiliate_action"
        )
        if len(affiliates) == 1:
            action.update(views=[(False, "form")], res_id=affiliates.id)
        else:
            action["domain"] = [("id", "in", affiliates.ids)]

        action["context"] = {
            "default_partner_id": self.id,
        }
        return action

    @api.depends("affiliates")
    def _compute_affiliate_count(self):
        for record in self:
            record.affiliate_count = len(record.affiliates)
