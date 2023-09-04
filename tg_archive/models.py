from odoo import api, models, fields


class GoogleAttachmentArchiveMixin(models.AbstractModel):
    _name = "google.attachment.archive.mixin"
    google_folder_id = fields.Char(readonly=True)
    attachment_archive_url = fields.Char(compute="_compute_attachment_archive_url", store=False, default="")

    @api.depends("google_folder_id")
    def _compute_attachment_archive_url(self):
        for record in self:
            if not record.google_folder_id:
                record.attachment_archive_url = ""
            else:
                record.attachment_archive_url = "https://drive.google.com/drive/folders/" + record.google_folder_id


class AccountMove(models.Model):
    _inherit = ["google.attachment.archive.mixin", "account.move"]
    _name = "account.move"
