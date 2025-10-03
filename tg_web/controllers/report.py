from odoo.http import route

from odoo.addons.web.controllers.report import ReportController


class TGReportController(ReportController):
    @route(website=False)
    def report_routes(self, *args, **kw):
        return super().report_routes(*args, **kw)
