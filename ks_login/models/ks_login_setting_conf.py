# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.translate import html_translate


class KsLogin(models.Model):
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
        record = super(KsLogin, self).default_get(vals_list)
        sup = self.env['res.config.settings'].sudo().search([])
        record['ks_website_id'] = sup.website_id
        return record

    @api.constrains('ks_is_active')
    def ks_active(self):
        ks_record = self.env['ks_login.setting.conf'].sudo().search([('id', '!=', self.id)])
        for rec in ks_record:
            if self.ks_is_active == True and rec.ks_website_id.id == self.ks_website_id.id and rec.ks_is_active == True:
                raise ValidationError(_('Please inactive other record with same website'))


    @api.model
    def create(self, vals):
        print('======================create')
        res = super(KsLogin, self).create(vals)
        if res.ks_fields_ids.ids:
            template = res.ks_update_template_fields()
            res['ks_template'] = template.id
        return res

    def write(self, vals):
        res = super(KsLogin, self).write(vals)
        for rec in self:
            if 'ks_template' not in vals:
                self.ks_update_template_fields(ks_template_id=rec['ks_template'])
        return res




    def ks_update_template_fields(self, ks_template_id=False):
        tem_fields = []
        ks_custom_ids = self.env['ir.ui.view'].sudo().search([('key', 'ilike', 'ks_login.ks_custom_layout_temp_')])
        # ks_conf_id = self.env['ks_login.setting.conf'].search([('ks_is_active', '=', True)], limit=1)
        if self.ks_fields_ids:
            temp = ''
            for rec in self.ks_fields_ids:
                ks_field_label = rec.ks_field_id.field_description
                ks_field_name = rec.ks_field_id.name
                ks_field_group_str = rec.ks_field_label.split(' ')
                ks_field_type = rec.ks_field_type
                ks_group = ''
                for ks_group_str in ks_field_group_str:
                    ks_group = ks_group +ks_group_str
                    print('ks_group', ks_group)
                ks_field_group = "field-"+ks_group
                print('ks_field_group--------', ks_field_group)
                if rec.ks_placeholder:
                    ks_placeholder = rec.ks_placeholder
                else:
                    ks_placeholder = ks_field_label
                if ks_field_type == 'many2one':
                    ks_field_relation = rec.ks_field_id.relation
                    ks_many_2_one_ids = self.env[ks_field_relation].sudo().search([])
                    ks_many2_one_arch = ''
                    for many_val in ks_many_2_one_ids:
                        ks_many2_one_arch += "<option t-att-value={} ><t t-esc={}></option>".format(many_val.id, many_val.name)
                    # arch_new = "<label for={} class ={}></label><select name={} placeholder={} t-attf-class='form-control form-control-sm' required='required' autofocus='autofocus' autocapitalize='off'><option value=''>{}</option>".format(ks_field_name, ks_field_label, ks_field_name, ks_placeholder, ks_field_label)
                    temp = "<select> " + ks_many2_one_arch + "</select>\n"
                else:
                    temp += """       <label for= """ + """ " """ + ks_field_name + """ " """ + """class ="col-form-label">""" + ks_field_label + """</label>\n""" \
                            + """       <input type=""" + """ " """ + ks_field_type + """ " """ + """placeholder=""" + """ " """ + ks_placeholder + """ " """ + """name=""" + """ " """ + ks_field_name + """ " """ + """t-att-value=""" + """ " """ + ks_field_name + """ " """ + """id=""" + """ " """ + ks_field_name + """ " """ + """class="form-control form-control-sm" required="required" autofocus="autofocus" autocapitalize="off"/>\n"""

                # ks_rec = list_val.append(temp)
            if not ks_custom_ids.ids:
                key = 'ks_login.ks_custom_layout_temp_'
                name = 'layout_template_'
            else:
                key = 'ks_login.ks_custom_layout_temp_' + str(len(ks_custom_ids.ids))
                name = 'layout_template_' + str(len(ks_custom_ids.ids))
            arch = "<div class='form-group'>" + temp + "</div>"
            if ks_template_id:
                ks_template_id.arch = arch
                ks_temp = ks_template_id
            else:
                ks_temp = self.env['ir.ui.view'].sudo().create({
                    'name': name,
                    'key': key,
                    'type': 'qweb',
                    'arch': arch
                })
            return ks_temp






        # tem_fields = []
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
                # temp_str_starting = """<xpath expr="//t[1]/div[2]/input[1]" position="after">\n"""
        #     #     temp_str_ending = """</xpath>"""
        #         temp_str_fields = """    <div class=""" + """ "form-group """ + ks_field_group + """ ">\n""" \
        #                          +"""       \t<label for= """+""" " """ + ks_group +""" " """ +"""class ="col-form-label">""" + ks_field_label + """</label>\n""" \
        #                          +"""       <input type="text" """ + """placeholder="""+""" " """ +ks_placeholder+""" " """+ """name="""+ """ " """+ks_group+ """ " """ + """t-att-value="""+""" " """+ks_group+""" " """ +"""id="""+""" " """+ks_group+""" " """ +"""class="form-control form-control-sm" required="required" autofocus="autofocus" autocapitalize="off"/>\n""" \
        #                          +"""    </div>\n"""
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







