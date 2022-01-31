# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError


class ks_login(models.Model):
    _name = 'ks_login.setting.conf'

    name = fields.Char("Name", required=True)
    ks_website_id = fields.Many2one('website', string="Website", required=True)
    ks_fields_ids = fields.One2many("ks_login.dynamic.fields", "ks_cr_model_id",
                                    string="Login Fields")
    ks_checkbox = fields.Selection([('image','Image'),('none','None')],'Image', default='none')
    ks_is_active = fields.Boolean("Active", default = False, required=True)
    ks_backgroud_img = fields.Binary("Background Image")
    ks_signup_content = fields.Html('Signup Content', translate=html_translate)
    ks_login_content =  fields.Html('Login Content', translate=html_translate)
    ks_pw_reset_content =  fields.Html('Reset Password Content', translate=html_translate)
    ks_template = fields.Many2one('ir.ui.view', readonly=True)

    @api.model
    def default_get(self, vals_list):
        record = super(ks_login,self).default_get(vals_list)
        sup = self.env['res.config.settings'].search([])
        record['ks_website_id'] = sup.website_id
        return record

    @api.constrains('ks_is_active')
    def ks_active(self):
        ks_record = self.env['ks_login.setting.conf'].search([('id', '!=', self.id)])
        for rec in ks_record:
            if self.ks_is_active == True and rec.ks_website_id.id == self.ks_website_id.id and rec.ks_is_active == True:
                raise ValidationError(_('Please inactive other record with same website'))


    @api.model
    def create(self, vals):
        print('======================create')
        res = super(ks_login, self).create(vals)
        if res.ks_fields_ids.ids:
            template = self.ks_update_template_fields()
            res['ks_template'] = template.id
        return res
    #
    # @api.multi
    # def write(self, vals):
    #     res = super(ks_login, self).write(vals)
    #     return res

    def ks_update_template_fields(self):
        ks_custom_ids = self.env['ir.ui.veiw'].search([('key', 'ilike', 'ks_login.ks_custom_layout_temp_')])
        if not ks_custom_ids.ids:
            key = 'ks_login.ks_custom_layout_temp_'
        else:
            key = 'ks_login.ks_custom_layout_temp_' + str(len(ks_custom_ids.ids))
        ks_temp = self.env['ir.ui.veiw'].sudo().create({
            'name': 'layout_template1',
            'key': key,
            'type': 'qweb',
            'arch':
                """    <div>
                <span>text place</span>
                </div>\n"""

        })
        return ks_temp
        tem_fields = []
        # ks_conf_id = self.env['ks_login.setting.conf'].search([('ks_is_active', '=', True)], limit=1)
        # if ks_conf_id:
        #     for rec in ks_conf_id.ks_fields_ids:
        #         print('rec--------', rec)
        #         ks_field_label = rec.ks_field_label
        #         ks_field_group_str = rec.ks_field_label.split(' ')
        #         print('ks_field_label-----','ks_field_group_str---', ks_field_group_str, ks_field_label)
        #         ks_group = ''
        #         for ks_group_str in ks_field_group_str:
        #             ks_group = ks_group +ks_group_str
        #             print('ks_group', ks_group)
        #         ks_field_group = "field-"+ks_group
        #         print('ks_field_group--------', ks_field_group)
        #         if rec.ks_placeholder:
        #             ks_placeholder = rec.ks_placeholder
        #         else:
        #             ks_placeholder =""
        #         print('ks_placeholder------', ks_placeholder)

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #     #     temp_str_starting = """<xpath expr="//t[1]/div[2]/input[1]" position="after">\n"""
        #     #     temp_str_ending = """</xpath>"""
        #     #     temp_str_fields = """    <div class=""" + """ "form-group """ + ks_field_group + """ ">\n""" \
        #     #                      +"""       \t<label for= """+""" " """ + ks_group +""" " """ +"""class ="col-form-label">""" + ks_field_label + """</label>\n""" \
        #     #                      +"""       <input type="text" """ + """placeholder="""+""" " """ +ks_placeholder+""" " """+ """name="""+ """ " """+ks_group+ """ " """ + """t-att-value="""+""" " """+ks_group+""" " """ +"""id="""+""" " """+ks_group+""" " """ +"""class="form-control form-control-sm" required="required" autofocus="autofocus" autocapitalize="off"/>\n""" \
        #     #                      +"""    </div>\n"""
        #     #     tem_fields.append(temp_str_fields)
        #     # ks_template_sign_up = self.env.ref('ks_login.signup_fields')
        #     # custom_fields = ""
        #     # for i in tem_fields:
        #     #     custom_fields = custom_fields + i
        #     # final_str = temp_str_starting + custom_fields + temp_str_ending
        #     # ks_template_sign_up.write({
        #     # 'arch': final_str,
        #     # })

    # def ks_update_content(self):
    #     ks_conf_id = self.search([('ks_is_active', '=', True)], limit=1)
    #     if ks_conf_id:
    #         ks_signin_content = ks_conf_id.ks_signup_content
    #         if ks_signin_content:
    #             ks_signin_temp = self.env.ref('ks_login.ks_signin_template')
    #             # ks_signin_temp = self.env.ref('web.frontend_layout')
    #             arc = """
    #                 <xpath expr="//div[last()]" position="inside">
    #                     <span style="color: rgb(160, 160, 160); font-family: Georgia,Times, serif; font-style: italic;">Hello</span>
    #                 </xpath>
    #             """
    #             ks_signin_temp.write({
    #                 'arch': arc,
    #             })







