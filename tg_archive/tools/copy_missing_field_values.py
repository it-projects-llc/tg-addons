from collections import defaultdict
import logging


_logger = logging.getLogger(__name__)


def method1(env, old_cr, company_id):
    records = env['account.move'].search([
        ("move_type", "=", "in_receipt"),
        ("company_id", "=", company_id),
        ("ref", "in", [False, ""]),
        ("partner_id", "!=", False),
    ])

    _logger.info("Using method 1")
    for receipt in records:
        old_cr.execute(
            "select id, reference, google_folder_id from account_voucher where date = %s and partner_id = %s and round(amount, 2) = %s",
            [receipt.invoice_date, receipt.partner_id.id, round(receipt.amount_total, 2)]
        )
        rows = old_cr.fetchall()
        if len(rows) == 1:
            row = rows[0]
            _logger.info("%s, %s copied using method 1" % (receipt.invoice_date, receipt,))
            receipt.write({
                "ref": row[1],
                "google_folder_id": row[2],
            })
            env.cr.commit()
        else:
            _logger.info("%s, %s skipped method 1: rows count %s, %s" % (receipt.invoice_date, receipt, len(rows), receipt.partner_id.name))

def method2(env, old_cr, company_id):
    records = env['account.move'].search([
        ("move_type", "=", "in_receipt"),
        ("company_id", "=", company_id),
        ("ref", "in", [False, ""]),
        ("partner_id", "!=", False),
    ])

    counters = defaultdict(int)

    _logger.info("Using method 2")
    for receipt in records:
        key = (receipt.invoice_date, receipt.partner_id.id, round(receipt.amount_total, 2))
        old_cr.execute(
            "select id, reference, google_folder_id from account_voucher where date = %s and partner_id = %s and round(amount, 2) = %s ORDER BY id DESC OFFSET %s LIMIT 1",
            list(key) + [counters[key]]
        )
        counters[key] += 1
        rows = old_cr.fetchall()
        if len(rows) == 1:
            row = rows[0]
            _logger.info("%s, %s copied using method 2" % (receipt.invoice_date, receipt,))
            receipt.write({
                "ref": row[1],
                "google_folder_id": row[2],
            })
            env.cr.commit()
        else:
            _logger.info("%s, %s skipped method 2: rows count %s" % (receipt.invoice_date, receipt, len(rows)))

def method3(env, old_cr, company_id):
    records = env['account.move'].search([
        ("move_type", "=", "in_receipt"),
        ("company_id", "=", company_id),
        ("google_folder_id", "=", False),
        ("ref", "not in", [False, ""]),
    ])

    _logger.info("Using method 3")
    for receipt in records:
        old_cr.execute(
            "select id, google_folder_id from account_voucher where date = %s and partner_id = %s and reference = %s and google_folder_id IS NOT NULL",
            [receipt.invoice_date, receipt.partner_id.id, receipt.ref],
        )
        rows = old_cr.fetchall()
        if len(rows) == 1:
            row = rows[0]
            _logger.info("%s, %s copied using method 3" % (receipt.invoice_date, receipt,))
            receipt.write({
                "google_folder_id": row[1],
            })
            env.cr.commit()
        else:
            _logger.info("%s, %s skipped method 3: rows count %s" % (receipt.invoice_date, receipt, len(rows)))

def method4(env, old_cr, company_id):
    records = env['account.move'].search([
        ("move_type", "=", "in_receipt"),
        ("company_id", "=", company_id),
        ("google_folder_id", "=", False),
        ("ref", "in", [False, ""]),
        ("name", "!=", "/"),
    ])

    _logger.info("Using method 4")
    for receipt in records:
        old_cr.execute(
            "select id, google_folder_id from account_voucher where number = %s and google_folder_id IS NOT NULL",
            [receipt.name],
        )
        rows = old_cr.fetchall()
        if len(rows) == 1:
            row = rows[0]
            _logger.info("%s, %s copied using method 4" % (receipt.invoice_date, receipt,))
            receipt.write({
                "google_folder_id": row[1],
            })
            env.cr.commit()
        else:
            _logger.info("%s, %s skipped method 4: rows count %s" % (receipt.invoice_date, receipt, len(rows)))
