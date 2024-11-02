def migrate(cr, installed_version):
    cr.execute("UPDATE pos_config SET hex_barcode = pos_rfid")
