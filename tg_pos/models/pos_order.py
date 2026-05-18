import logging

from odoo import SUPERUSER_ID, api, fields, models, registry
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero

from .account_move import sentinel

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    partner_id = fields.Many2one(ondelete="restrict")

    def _generate_pos_order_invoice(self):
        res = super()._generate_pos_order_invoice()
        orders = self.filtered("config_id.auto_duplicate_invoices")
        later_duplicate = self.env["account.move"].sudo()

        for order in orders.sudo():
            if not order.account_move:
                continue

            move = order.account_move

            if float_is_zero(move.amount_total, move.currency_id.rounding):
                continue

            try:
                move._duplicate_invoice_check()

            except ValidationError:
                if not move.duplicated_fiscal_invoice:
                    move.must_be_duplicated = True
                continue

            if order.config_id.debug_auto_duplicate_invoices:
                move._duplicate_invoice_inner()
            else:
                move.must_be_duplicated = True
                later_duplicate |= move

        dbname = self.env.cr.dbname
        ctx = self.env.context
        later_duplicate_ids = later_duplicate.ids

        @self.env.cr.postcommit.add
        def duplicate_invoices_after_commit():
            db_registry = registry(dbname)
            for invoice_id in later_duplicate_ids:
                with db_registry.cursor() as cr:
                    env = api.Environment(cr, SUPERUSER_ID, ctx)
                    move = env["account.move"].browse(invoice_id)
                    try:
                        move._duplicate_invoice_inner()
                        move.must_be_duplicated = False
                    except Exception as e:
                        _logger.exception(str(e))
                        cr.rollback()

        return res

    def _prepare_tax_base_line_values(self, sign=1):
        if sign < 0 and self.env.context.get("sign_only_positive") == sentinel:
            sign = -1 * sign
        return super()._prepare_tax_base_line_values(sign)
