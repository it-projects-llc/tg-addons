from odoo import models


class IrQweb(models.AbstractModel):
    _inherit = "ir.qweb"

    def _prepare_environment(self, values):
        # TODO: remove this in 19.0+
        # t-cache is removed there
        irQweb = super()._prepare_environment(values)
        return irQweb.with_context(is_t_cache_disabled=True)
