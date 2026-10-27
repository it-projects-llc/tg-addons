from odoo import models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _render_template(self, template, values=None):
        if isinstance(template, str) and template.startswith("website"):
            self = self.with_context(tz="America/Panama")
        return super()._render_template(template, values)
