# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ks_dynamic_fields(models.Model):
    _name = 'ks_login.dynamic.fields'

    ks_cr_model_id = fields.Many2one('ks_login.setting.conf', string="Login Model",)
    ks_field_id = fields.Many2one('ir.model.fields', "Field Name", domain=[('model', 'in', ['res.partner']), ('ttype', 'in', ['char', 'integer', 'float', 'boolean', 'text', 'selection', 'one2many', 'many2one', 'many2many'])])
    ks_field_label = fields.Char("Field Label")
    ks_placeholder = fields.Char('Placeholder')
    ks_field_type = fields.Selection([("binary", "binary"), ("boolean", "boolean"), ("char", "Char"), ("date", "Date"), ("datetime", "Datetime"), ("float", "Float"),
                                      ("html", "Html"), ("integer", "Integer"), ("many2one", "Many2one"), ("many2many", "Many2many"),
                                      ("monetary", "Monetary"), ("one2many", "One2many"), ("reference", "Reference"), ("selection", "Selection"), ("text", "Text")], string="Fields Type")
    ks_sequence = fields.Integer("Sequence")
    ks_no_of_column = fields.Selection([
        ('one', "1"),
        ('two', "2"),
    ], string="Number of column")
    ks_is_required = fields.Boolean("required")
    ks_description = fields.Text(string="Description")

    @api.onchange('ks_field_id')
    def get_fields_records(self):
        self.ks_field_label = self.ks_field_id.field_description
        self.ks_field_type = self.ks_field_id.ttype




