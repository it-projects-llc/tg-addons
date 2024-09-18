from odoo import models


class MergePartnerAutomatic(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    # removed _merge function since
    # https://github.com/odoo/odoo/commit/0148f19f67f8725ae9bea7c208f09b4676652cc0
