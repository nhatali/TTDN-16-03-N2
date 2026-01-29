#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để fix các action window đang tham chiếu đến model không tồn tại
Chạy script này trong Odoo shell hoặc với python odoo-bin shell
"""

import odoo
from odoo import api, SUPERUSER_ID

def fix_invalid_actions():
    """Xóa hoặc vô hiệu hóa các action window đang tham chiếu model không tồn tại"""
    
    # Khởi tạo Odoo
    odoo.tools.config.parse_config(['--database=your_database_name'])  # Thay đổi tên database
    
    with odoo.api.Environment.manage():
        env = api.Environment(odoo.registry(odoo.tools.config['db_name']), SUPERUSER_ID, {})
        
        # Lấy danh sách tất cả các model hợp lệ
        valid_models = set(env.registry.keys())
        
        # Tìm các action window có res_model không tồn tại
        invalid_actions = env['ir.actions.act_window'].search([])
        fixed_count = 0
        
        for action in invalid_actions:
            if action.res_model and action.res_model not in valid_models:
                print(f"Tìm thấy action không hợp lệ: ID={action.id}, name={action.name}, res_model={action.res_model}")
                
                # Option 1: Xóa action (uncomment nếu muốn xóa)
                # action.unlink()
                # print(f"  -> Đã xóa action ID {action.id}")
                
                # Option 2: Vô hiệu hóa action bằng cách xóa res_model
                action.write({'res_model': False})
                print(f"  -> Đã vô hiệu hóa action ID {action.id} (xóa res_model)")
                fixed_count += 1
        
        print(f"\nTổng cộng đã fix {fixed_count} action(s)")
        
        # Commit changes
        env.cr.commit()

if __name__ == '__main__':
    print("Script fix invalid actions")
    print("Lưu ý: Cần thay đổi tên database trong script trước khi chạy")
    print("Hoặc chạy trong Odoo shell với: python odoo-bin shell -d your_database")
