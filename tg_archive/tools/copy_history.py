import logging

# 653843

_logger = logging.getLogger(__name__)


def method1(env, old_cr):
    records = env["account.move"].search(
        [
            ("move_type", "in", ["in_receipt", "out_receipt"]),
            ("google_folder_id", "!=", False),
        ]
    )

    _logger.info("Using method 1")
    for record in records:
        old_cr.execute(
            "select id from account_voucher where google_folder_id = %s",
            [record.google_folder_id],
        )
        rows = old_cr.fetchall()
        if len(rows) == 1:
            old_res_id = rows[0][0]
            env.cr.execute(
                "UPDATE mail_message SET (res_id,model) = (%s,%s) "
                "WHERE (res_id, model) = (%s, 'account.voucher')",  # noqa: B950
                [record.id, record._name, old_res_id],
            )
            env.cr.commit()
        else:
            _logger.info(
                f"{record.invoice_date}, {record} "
                f"skipped method 1: rows count {len(rows)}"
            )


def method2(env, old_cr):
    records = env["account.move"].search(
        [
            ("move_type", "in", ["in_receipt", "out_receipt"]),
            ("google_folder_id", "=", False),
            ("name", "!=", "/"),
        ]
    )

    _logger.info("Using method 2")
    for record in records:
        old_cr.execute(
            "select id from account_voucher " "where name = %s", [record.name]
        )
        rows = old_cr.fetchall()
        if len(rows) == 1:
            old_res_id = rows[0][0]
            env.cr.execute(
                "UPDATE mail_message SET (res_id,model) = (%s,%s) "
                "WHERE (res_id, model) = (%s, 'account.voucher')",  # noqa: B950
                [record.id, record._name, old_res_id],
            )
            env.cr.commit()
        else:
            _logger.info(
                f"{record.invoice_date}, {record} "
                f"skipped method 2: rows count {len(rows)}"
            )


def method3(env, old_cr):
    records = env["account.move"].search(
        [
            ("move_type", "in", ["in_receipt", "out_receipt"]),
            ("google_folder_id", "=", False),
            ("name", "=", "/"),
            ("ref", "not in", [False, ""]),
        ]
    )

    _logger.info("Using method 3")
    for record in records:
        old_cr.execute(
            "select id from account_voucher " "where reference = %s", [record.ref]
        )
        rows = old_cr.fetchall()
        if len(rows) == 1:
            old_res_id = rows[0][0]
            env.cr.execute(
                "UPDATE mail_message SET (res_id,model) = (%s,%s) "
                "WHERE (res_id, model) = (%s, 'account.voucher')",  # noqa: B950
                [record.id, record._name, old_res_id],
            )
            env.cr.commit()
        else:
            _logger.info(
                f"{record.invoice_date}, {record} "
                f"skipped method 3: rows count {len(rows)}"
            )
