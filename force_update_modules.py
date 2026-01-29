#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để force update module list trong Odoo
Chạy script này khi module không hiển thị trong Apps
"""

import os
import sys

# Thêm đường dẫn Odoo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'odoo'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'addons'))

import odoo
from odoo import api, SUPERUSER_ID

def update_module_list():
    """Update module list trong database"""
    
    # Đọc config
    config_file = 'odoo.conf'
    if not os.path.exists(config_file):
        print(f"❌ Không tìm thấy file {config_file}")
        return
    
    # Parse config để lấy database name
    db_name = None
    with open(config_file, 'r') as f:
        for line in f:
            if line.startswith('db_name'):
                db_name = line.split('=')[1].strip()
                break
    
    if not db_name:
        # Thử các tên database phổ biến
        db_name = 'odoo'
        print(f"⚠️  Không tìm thấy db_name trong config, dùng mặc định: {db_name}")
    
    print(f"📦 Database: {db_name}")
    print("🔄 Đang update module list...")
    
    try:
        # Khởi tạo Odoo
        odoo.tools.config.parse_config([f'--config={config_file}'])
        
        with odoo.api.Environment.manage():
            env = api.Environment(odoo.registry(db_name), SUPERUSER_ID, {})
            
            # Update module list
            updated, added = env['ir.module.module'].update_list()
            
            print(f"✅ Hoàn thành!")
            print(f"   - Updated: {updated} modules")
            print(f"   - Added: {added} modules")
            
            # Kiểm tra các module của chúng ta
            modules_to_check = ['nhan_su', 'cham_cong', 'tien_luong']
            print("\n📋 Kiểm tra module:")
            
            for module_name in modules_to_check:
                module = env['ir.module.module'].search([('name', '=', module_name)], limit=1)
                if module:
                    state = module.state
                    installable = '✅' if module.state != 'uninstalled' or module.installable else '❌'
                    print(f"   {installable} {module_name}: state={state}, installable={module.installable}")
                else:
                    print(f"   ❌ {module_name}: KHÔNG TÌM THẤY")
            
            env.cr.commit()
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("FORCE UPDATE MODULE LIST")
    print("=" * 60)
    update_module_list()
    print("=" * 60)
    print("\n💡 Sau khi chạy script này:")
    print("   1. Restart Odoo server")
    print("   2. Vào Apps và tìm kiếm module")
    print("=" * 60)
