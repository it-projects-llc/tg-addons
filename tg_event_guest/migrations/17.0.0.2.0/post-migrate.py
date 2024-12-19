def migrate(cr, installed_version):
    from odoo import SUPERUSER_ID, api

    env = api.Environment(cr, SUPERUSER_ID, {})

    env.ref("tg_event_guest.email_template_partner").lang = False
