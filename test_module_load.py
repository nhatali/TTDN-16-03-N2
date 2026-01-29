#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test xem module có load được không
"""

import sys
import os

# Test import module
modules_to_test = [
    'addons.btl.nhan_su',
    'addons.btl.cham_cong',
    'addons.btl.tien_luong',
]

print("=" * 60)
print("TEST MODULE LOAD")
print("=" * 60)

for module_name in modules_to_test:
    try:
        # Test import __init__
        module_path = module_name.replace('.', '/')
        init_file = f"{module_path}/__init__.py"
        
        if os.path.exists(init_file):
            print(f"✅ {module_name}: __init__.py tồn tại")
            
            # Test import models
            models_init = f"{module_path}/models/__init__.py"
            if os.path.exists(models_init):
                print(f"   ✅ models/__init__.py tồn tại")
            else:
                print(f"   ❌ models/__init__.py KHÔNG tồn tại")
        else:
            print(f"❌ {module_name}: __init__.py KHÔNG tồn tại")
            
    except Exception as e:
        print(f"❌ {module_name}: Lỗi - {e}")

print("=" * 60)
