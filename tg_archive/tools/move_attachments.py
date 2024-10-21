# pylint: disable=consider-using-f-string
# pylint: disable=logging-not-lazy
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-manifest-dependency


import logging
import os

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PATH = "/tmp/move_attachments"

_logger = logging.getLogger(__file__)
creds, _ = google.auth.default()
service = build("drive", "v3", credentials=creds)
company_folder_id = os.environ["COMPANY_FOLDER_ID"]


def _create_folder(name, parent_id):
    file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    obj = service.files().create(body=file_metadata, fields="id").execute()
    return obj["id"]


def _create_file(name, input_path, mimetype, parent_id):
    file_metadata = {"name": name, "parents": [parent_id]}

    media = MediaFileUpload(input_path, mimetype=mimetype)
    obj = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    return obj.get("id")


def get_directory_id(record):
    if not record:
        raise ValueError("record is falsy")

    fid = record.google_folder_id
    if fid:
        return fid

    fid = _create_folder(record._name + "_" + str(record.id), company_folder_id)
    record.google_folder_id = fid
    record.env.cr.commit()

    return fid


def upload_attachments(attachments, directory_id):
    for attachment in attachments:
        if len(attachments) == 1:
            remote_attachment_name = attachment.name
        else:
            remote_attachment_name = str(attachment.id) + "_" + attachment.name

        _logger.info("uploading %s to %s..." % (attachment, directory_id))
        _, input_path = attachment._get_path(None, attachment.checksum)
        if not os.path.isfile(input_path):
            _logger.warning(
                "Skipping %s. %s is not a file"
                % (
                    attachment,
                    input_path,
                )
            )
            continue
        fid = _create_file(
            remote_attachment_name,
            input_path,
            attachment.mimetype or None,
            directory_id,
        )
        if not fid:
            raise Exception("Something happened, when upload file")

    try:
        attachments.unlink()
    except IOError as e:
        _logger.warning("Problems when unlinking %s: %s" % (attachments, str(e)))

    attachments.env.cr.commit()
    attachments._gc_file_store()


def init_hacks():
    from odoo.addons.base.models.ir_attachment import IrAttachment

    def _same_content_hacked(self, *args, **kw):
        return True

    # this will make _get_path to accept None
    IrAttachment._same_content = _same_content_hacked


def move_attachments(env, company_id, last_date):
    init_hacks()

    env.cr.execute(
        """
SELECT array_agg(json_build_object('res_id', t.res_id, 'res_model', t.res_model, 'attachment_ids', t.attachment_ids))
FROM (
    SELECT a.res_id, a.res_model, array_agg(a.id) AS attachment_ids
    FROM ir_attachment a
    LEFT JOIN account_move j ON j.id = a.res_id
    WHERE a.res_model = 'account.move'
    AND a.res_field IS NULL
    AND a.checksum IS NOT NULL
    AND j.company_id = %s
    AND j.invoice_date <= %s
    GROUP BY a.res_id, a.res_model
) t
    """,  # noqa: B950
        [company_id, last_date],
    )
    objs = env.cr.fetchone()[0] or []

    for obj in objs:
        record = env[obj["res_model"]].browse(obj["res_id"])
        attachments = env["ir.attachment"].browse(obj["attachment_ids"])

        _logger.info("record %s, attachments %s" % (record, attachments))
        record_directory_id = get_directory_id(record)

        _logger.info("uploading %s attachments..." % len(attachments))
        upload_attachments(attachments, record_directory_id)
