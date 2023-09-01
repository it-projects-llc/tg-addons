from odoo import api, models, fields


class GoogleAttachmentArchiveMixin():
    google_folder_id = fields.Char(readonly=True)
    attachment_archive_url = fields.Char(compute="_compute_attachment_archive_url", store=False)

    @api.depends("google_folder_id")
    def _compute_attachment_archive_url(self):
        for record in self:
            if not record.google_folder_id:
                record.attachment_archive_url = False
            else:
                record.attachment_archive_url = "https://drive.google.com/drive/folders/" + record.google_folder_id


class AccountVoucher(GoogleAttachmentArchiveMixin, models.Model):
    _inherit = "account.voucher"


class AccountInvoice(GoogleAttachmentArchiveMixin, models.Model):
    _inherit = "account.invoice"
