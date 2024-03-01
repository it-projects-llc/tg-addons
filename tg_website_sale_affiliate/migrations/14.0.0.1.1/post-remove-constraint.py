def migrate(cr, installed_version):
    cr.execute(
        """
ALTER TABLE sale_affiliate
DROP CONSTRAINT IF EXISTS sale_affiliate_partner_id_unique
    """
    )
