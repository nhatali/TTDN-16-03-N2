#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để test xem module có được Odoo nhận diện không
"""

import sys
import os

# Thêm đường dẫn Odoo vào sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'odoo'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'addons'))

try:
    import odoo
    from odoo.modules.module import get_module_path
    
    # Kiểm tra các module
    modules = ['nhan_su', 'cham_cong', 'tien_luong']
    
    print("=" * 50)
    print("KIỂM TRA MODULE")
    print("=" * 50)
    
    for module_name in modules:
        try:
            module_path = get_module_path(module_name, downloaded=True)
            if module_path:
                print(f"✅ {module_name}: Tìm thấy tại {module_path}")
                
                # Kiểm tra __manifest__.py
                manifest_path = os.path.join(module_path, '__manifest__.py')
                if os.path.exists(manifest_path):
                    print(f"   ✅ __manifest__.py tồn tại")
                else:
                    print(f"   ❌ __manifest__.py KHÔNG tồn tại")
                
                # Kiểm tra __init__.py
                init_path = os.path.join(module_path, '__init__.py')
                if os.path.exists(init_path):
                    print(f"   ✅ __init__.py tồn tại")
                else:
                    print(f"   ❌ __init__.py KHÔNG tồn tại")
            else:
                print(f"❌ {module_name}: KHÔNG tìm thấy")
        except Exception as e:
            print(f"❌ {module_name}: Lỗi - {e}")
    
    print("=" * 50)
    
except ImportError as e:
    print(f"Lỗi import Odoo: {e}")
    print("Hãy chạy script này từ thư mục Business-Internship")
