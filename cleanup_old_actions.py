#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để cleanup các action window cũ tham chiếu đến model không tồn tại
"""

import os
import sys

# Thêm đường dẫn
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'odoo'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'addons'))

try:
    import odoo
    from odoo import api, SUPERUSER_ID
    
    config_file = 'odoo.conf'
    db_name = 'odoo'
    
    print("=" * 60)
    print("CLEANUP OLD ACTIONS")
    print("=" * 60)
    
    odoo.tools.config.parse_config([f'--config={config_file}'])
    
    with odoo.api.Environment.manage():
        env = api.Environment(odoo.registry(db_name), SUPERUSER_ID, {})
        
        # Lấy danh sách model hợp lệ
        valid_models = set(env.registry.keys())
        
        print(f"\nDatabase: {db_name}")
        print(f"Số model hợp lệ: {len(valid_models)}")
        
        # Tìm các action window có res_model không tồn tại
        invalid_actions = env['ir.actions.act_window'].search([])
        fixed_count = 0
        
        print("\nĐang tìm các action không hợp lệ...")
        
        for action in invalid_actions:
            if action.res_model and action.res_model not in valid_models:
                print(f"\n❌ Tìm thấy action không hợp lệ:")
                print(f"   ID: {action.id}")
                print(f"   Name: {action.name}")
                print(f"   res_model: {action.res_model}")
                
                # Vô hiệu hóa action bằng cách xóa res_model
                action.write({'res_model': False})
                print(f"   ✅ Đã vô hiệu hóa (xóa res_model)")
                fixed_count += 1
        
        if fixed_count > 0:
            env.cr.commit()
            print(f"\n✅ Đã fix {fixed_count} action(s)")
        else:
            print("\n✅ Không có action nào cần fix")
        
        print("\n" + "=" * 60)
        print("Hoàn thành! Hãy restart Odoo server và thử lại.")
        print("=" * 60)
        
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
