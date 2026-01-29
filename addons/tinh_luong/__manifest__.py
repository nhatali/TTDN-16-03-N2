# -*- coding: utf-8 -*-
{
    'name': 'Tính Lương',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Quản lý tính lương dựa trên chấm công',
    'description': """
        Module tính lương tự động:
        - Tích hợp với module nhân sự
        - Tích hợp với module chấm công
        - Tính lương theo công thức: Lương CB + Thưởng - Phạt
    """,
    'depends': ['base', 'nhan_su', 'cham_cong'],
    'data': [
        'security/ir.model.access.csv',
        'views/ky_luong.xml',
        'views/bang_luong.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
