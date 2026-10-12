from odoo import models

class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_pos_config(self):
        result = super()._loader_params_pos_config()
        if result['search_params'].get('fields'):
            result['search_params']['fields'].append('pos_max_split_orders')
        return result
