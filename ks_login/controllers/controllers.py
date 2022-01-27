# -*- coding: utf-8 -*-
# from odoo import http


import logging
from datetime import datetime

import werkzeug
from odoo import _, http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from openerp.http import request
from werkzeug.urls import iri_to_uri


class KsAuthSignupHome(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        sup = super(KsAuthSignupHome, self).web_auth_signup(*args, **kw)
        vals = request.website
        record = request.env['ks_login.setting.conf'].search([('ks_website_id', '=', vals.id), ('ks_is_active', '=', True)]).ks_template.key
        sup.qcontext['fields_xml'] = request.env.ref(record)
        response = request.render('ks_login.ks_signup', sup.qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
