from odoo.http import request, route

from odoo.addons.point_of_sale.controllers.main import PosController


class PosControllerRFID(PosController):
    @route()
    def pos_web(self, config_id=False, **kw):
        res = super().pos_web(config_id, **kw)
        if not config_id:
            return res

        config = request.env["pos.config"].sudo().browse(int(config_id))
        res.qcontext["session_info"]["pos_hex_barcode"] = config.hex_barcode
        return res
