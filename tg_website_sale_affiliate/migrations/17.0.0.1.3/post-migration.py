def migrate(cr, installed_version):
    cr.execute(
        """
UPDATE loyalty_program
SET program_type = 'promo_code'
WHERE id IN (
    SELECT code_promo_program_id
    FROM sale_affiliate
) AND program_type = 'promotion'
    """
    )
