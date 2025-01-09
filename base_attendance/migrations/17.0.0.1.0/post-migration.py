def migrate(cr, installed_version):
    from odoo import SUPERUSER_ID, api

    cr.execute(
        """
SELECT array_agg(DISTINCT partner_id) FROM res_partner_attendance
    """
    )

    partner_ids = cr.fetchone()[0] or []
    env = api.Environment(cr, SUPERUSER_ID, {"tracking_disable": True})
    env["res.partner"].browse(partner_ids)._create_employees()

    OldAttendances = env["res.partner.attendance"]
    Attendances = env["hr.attendance"]

    rows = OldAttendances.search([], order="id")

    for row in rows:
        old_id = row.id
        partner = row.partner_id
        check_in = row.check_in
        check_out = row.check_out
        employee = partner.employee_ids[0]

        last_attendance_before_check_in = Attendances.search(
            [
                ("employee_id", "=", employee.id),
                ("check_in", "<=", check_in),
            ],
            order="check_in desc",
            limit=1,
        )
        if (
            last_attendance_before_check_in
            and last_attendance_before_check_in.check_out
            and last_attendance_before_check_in.check_out > check_in
        ):
            continue

        last_attendance_before_check_out = Attendances.search(
            [
                ("employee_id", "=", employee.id),
                ("check_in", "<", check_out),
            ],
            order="check_in desc",
            limit=1,
        )
        if (
            last_attendance_before_check_out
            and last_attendance_before_check_in != last_attendance_before_check_out
        ):
            continue

        attendance = Attendances.create(
            {
                "employee_id": employee.id,
                "check_in": check_in,
                "check_out": check_out,
            }
        )
        old_attendance = OldAttendances.browse(old_id)
        old_attendance.new_id = attendance.id
