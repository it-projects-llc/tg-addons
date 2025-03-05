def post_load():
    from ast import literal_eval

    from odoo.addons.website.models.res_users import Command, ResUsers, api, request

    @api.model
    def _signup_create_user(self, values):
        current_website = self.env['website'].get_current_website()
        # Note that for the moment, portal users can connect to all websites of
        # all companies as long as the specific_user_account setting is not
        # activated.
        values['company_id'] = current_website.company_id.id
        values['company_ids'] = [Command.link(current_website.company_id.id)]

        # <--- changes start
        template_user_id = literal_eval(self.env['ir.config_parameter'].sudo().get_param('base.template_portal_user_id', 'False'))
        template_user = self.browse(template_user_id)
        for company in template_user.company_ids:
            values["company_ids"].append((4, company.id))
        # <---- changes end

        if request and current_website.specific_user_account:
            values['website_id'] = current_website.id
        new_user = super(ResUsers, self)._signup_create_user(values)
        return new_user

    ResUsers._signup_create_user = _signup_create_user
