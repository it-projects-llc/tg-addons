import logging

_logger = logging.getLogger(__name__)


def post_load():

    from odoo.addons.base.wizard.base_partner_merge import (
        Command,
        MergePartnerAutomatic,
        UserError,
        _,
    )

    def _merge(self, partner_ids, dst_partner=None, extra_checks=True):
        """ private implementation of merge partner
            :param partner_ids : ids of partner to merge
            :param dst_partner : record of destination res.partner
            :param extra_checks: pass False to bypass extra sanity check (e.g. email address)
        """
        # super-admin can be used to bypass extra checks
        if self.env.is_admin():
            extra_checks = False

        Partner = self.env['res.partner']
        partner_ids = Partner.browse(partner_ids).exists()
        if len(partner_ids) < 2:
            return

        if len(partner_ids) > 3:
            raise UserError(_("For safety reasons, you cannot merge more than 3 contacts together. You can re-open the wizard several times if needed."))

        # check if the list of partners to merge contains child/parent relation
        child_ids = self.env['res.partner']
        for partner_id in partner_ids:
            child_ids |= Partner.search([('id', 'child_of', [partner_id.id])]) - partner_id
        if partner_ids & child_ids:
            raise UserError(_("You cannot merge a contact with one of his parent."))

        # check if the list of partners to merge are linked to more than one user
        # <---- changed here
        # removed linked user check

        if extra_checks and len(set(partner.email for partner in partner_ids)) > 1:
            raise UserError(_("All contacts must have the same email. Only the Administrator can merge contacts with different emails."))

        # remove dst_partner from partners to merge
        if dst_partner and dst_partner in partner_ids:
            src_partners = partner_ids - dst_partner
        else:
            ordered_partners = self._get_ordered_partner(partner_ids.ids)
            dst_partner = ordered_partners[-1]
            src_partners = ordered_partners[:-1]
        _logger.info("dst_partner: %s", dst_partner.id)

        # Make the company of all related users consistent with destination partner company
        if dst_partner.company_id:
            partner_ids.mapped('user_ids').sudo().write({
                'company_ids': [Command.link(dst_partner.company_id.id)],
                'company_id': dst_partner.company_id.id
            })

        # <--- changes start
        src_users = src_partners.with_context(active_test=False).user_ids
        dst_users = dst_partner.with_context(active_test=False).user_ids
        if (dst_users and src_users) or (len(src_users) > 1):
            src_users.write({
                "partner_id": dst_partner.id,
                "active": False,
            })
        # <--- changes end

        # call sub methods to do the merge
        self._update_foreign_keys(src_partners, dst_partner)
        self._update_reference_fields(src_partners, dst_partner)
        self._update_values(src_partners, dst_partner)

        self.env.add_to_compute(dst_partner._fields['partner_share'], dst_partner)

        self._log_merge_operation(src_partners, dst_partner)

        # delete source partner, since they are merged
        src_partners.unlink()

    MergePartnerAutomatic._merge = _merge
