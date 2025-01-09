from odoo import _, models


class Partner(models.Model):
    _inherit = "res.partner"

    def _create_employees(self):
        company_id = self.env.company.id

        Employees = self.sudo().env["hr.employee"]
        already_has_employee = Employees.search(
            [
                ("work_contact_id", "in", self.ids),
                ("company_id", "=", company_id),
            ]
        ).mapped("work_contact_id")

        for partner in self - already_has_employee:
            if partner.user_ids:
                for user in partner.user_ids:
                    user.action_create_employee()
            else:
                Employees.create(
                    {
                        "name": partner.name,
                        "company_id": company_id,
                        "work_contact_id": partner.id,
                    }
                )

        return {
            "name": _("Related Employees"),
            "type": "ir.actions.act_window",
            "res_model": "hr.employee",
            "view_mode": "tree",
            "domain": [
                ("id", "in", self.employee_ids.ids),
                ("company_id", "=", company_id),
            ],
        }
