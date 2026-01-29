# -*- coding: utf-8 -*-
{
    'name': "cham_cong",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'nhan_su'
    ],

    # External dependencies
    'external_dependencies': {
        'python': ['face_recognition', 'PIL', 'numpy'],
    },

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/dang_ky_ca_lam_theo_ngay.xml',
        'views/bang_cham_cong.xml',
        'views/dot_dang_ky.xml',
        'views/don_tu.xml',
        'views/face_attendance_view.xml',
        'views/menu.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'cham_cong/static/src/js/face_attendance.js',
            'cham_cong/static/src/css/face_attendance.css',
        ],
        'web.assets_qweb': [
            'cham_cong/static/src/xml/face_attendance_templates.xml',
        ],
    },
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
