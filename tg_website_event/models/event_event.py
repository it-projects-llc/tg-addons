from odoo import models
from odoo.tools import config


class Event(models.Model):
    _inherit = "event.event"

    def _is_auto_popup_enabled(self):
        return not config["test_enable"]
