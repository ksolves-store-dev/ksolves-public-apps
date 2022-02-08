# -*- coding: utf-8 -*-
{
    'name': "ks_login",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ks_loging_setting_conf.xml',
        'views/templates.xml',
        # 'views/left_login_template.xml',
        'views/template_signup.xml',
        'views/assets.xml',
        # 'views/ks_signin_templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/ks_background_template.xml',


    ]
}
