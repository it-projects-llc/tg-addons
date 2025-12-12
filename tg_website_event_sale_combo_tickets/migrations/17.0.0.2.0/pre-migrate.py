def migrate(cr, installed_version):
    cr.execute(
        "ALTER TABLE event_question RENAME COLUMN is_shuttle_ticket TO is_shuttle"
    )
