# -*- coding: utf-8 -*-
# from odoo import http


import logging
from datetime import datetime
import base64
from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from openerp.http import request, route
from werkzeug.utils import redirect




class KsAuthSignupHome(AuthSignupHome):

    # @http.route('/web/login', type='http', auth="none")
    # def web_login(self, redirect=None, **kw):
    #     sup = super(KsAuthSignupHome, self).web_login(redirect=None, **kw)
    #     response = request.render('ks_login.login', sup.values)
    #     response.headers['X-Frame-Options'] = 'DENY'
    #     return response

    # this is for background image of login page
    @route(['/login_page/background'], type='http', auth="none")
    def login_background(self, **post):
        ks_background = ''
        user = request.env.user
        bg_image = request.env['ks_login.setting.conf'].sudo().search([('ks_is_active', '=', True)], limit=1).ks_background_img
        if bg_image:
            image = base64.b64decode(bg_image)
        else:
            return redirect(ks_background)
        return request.make_response(
            image, [('Content-Type', 'image')])

    @route(['/signup_page/background'], type='http', auth="none")
    def signup_background(self, **post):
        ks_background = ''
        user = request.env.user
        bg_image = request.env['ks_login.setting.conf'].sudo().search([('ks_is_active', '=', True)], limit=1).ks_background_img
        if bg_image:
            image = base64.b64decode(bg_image)
        else:
            return redirect(ks_background)
        return request.make_response(
            image, [('Content-Type', 'image')])



    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        sup = super(KsAuthSignupHome, self).web_auth_signup(*args, **kw)
        vals = request.website
        record = request.env['ks_login.setting.conf'].sudo().search([('ks_website_id', '=', vals.id)]).ks_template.key
        sup.qcontext['fields_xml'] = record
        response = request.render('ks_login.ks_signup', sup.qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response



    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        record = request.env['ks_login.setting.conf'].sudo().search([('ks_is_active', '=', True)], limit=1)
        ks_new = []
        ks_val = []
        valu_dict = {}

        for rec in record.ks_fields_ids:
            field = ' ' + rec.ks_field_id.name + ' '
            field_origin = rec.ks_field_id.name
            ks_new.append(field_origin)
            if field in qcontext:
                if qcontext[field]:
                    var = qcontext[field]
                    ks_val.append(var)
                    qcontext.pop(field)
        valu = zip(tuple(ks_new), tuple(ks_val))
        valu_dict = dict(valu)
        ks_tuple_key = ['login', 'name', 'password'] + ks_new
        qcontext.update(valu_dict)
        values = {key: qcontext.get(key) for key in ks_tuple_key}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()





