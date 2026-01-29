#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra module có trong database không
"""

import os
import sys

# Thêm đường dẫn
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'odoo'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'addons'))

try:
    import odoo
    from odoo import api, SUPERUSER_ID
    
    # Đọc config
    config_file = 'odoo.conf'
    db_name = 'odoo'
    
    print("=" * 60)
    print("KIỂM TRA MODULE TRONG DATABASE")
    print("=" * 60)
    
    # Khởi tạo Odoo
    odoo.tools.config.parse_config([f'--config={config_file}'])
    
    with odoo.api.Environment.manage():
        env = api.Environment(odoo.registry(db_name), SUPERUSER_ID, {})
        
        # Tìm các module
        modules_to_check = ['nhan_su', 'cham_cong', 'tien_luong']
        
        print(f"\nDatabase: {db_name}\n")
        
        for module_name in modules_to_check:
            module = env['ir.module.module'].search([('name', '=', module_name)], limit=1)
            if module:
                print(f"✅ {module_name}:")
                print(f"   - State: {module.state}")
                print(f"   - Installable: {module.installable}")
                print(f"   - Application: {module.application}")
                print(f"   - Summary: {module.summary or 'N/A'}")
            else:
                print(f"❌ {module_name}: KHÔNG TÌM THẤY trong database")
        
        print("\n" + "=" * 60)
        print("Nếu module có state='uninstalled', bạn có thể cài đặt")
        print("Nếu không thấy module, cần update module list lại")
        print("=" * 60)
        
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
