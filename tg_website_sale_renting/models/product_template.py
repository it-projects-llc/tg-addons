from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _get_default_start_date(self, *args, **kw):
        company = self.company_id or self.env.company
        return fields.Datetime.to_datetime(
            company.renting_default_start_date
        ) or super()._get_default_start_date(*args, **kw)

    @api.model
    def _get_default_end_date(self, *args, **kw):
        company = self.company_id or self.env.company
        return fields.Datetime.to_datetime(
            company.renting_default_end_date
        ) or super()._get_default_end_date(*args, **kw)

    def _get_renting_min_start_date(self):
        company = self.company_id or self.env.company
        return fields.Datetime.to_datetime(company.renting_min_start_date)

    def _get_renting_max_end_date(self):
        company = self.company_id or self.env.company
        return fields.Datetime.to_datetime(company.renting_max_end_date)
