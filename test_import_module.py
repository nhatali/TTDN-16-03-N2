#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test import module để tìm lỗi cụ thể
"""

import sys
import os

# Thêm đường dẫn
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'odoo'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'addons'))

print("=" * 60)
print("TEST IMPORT MODULE")
print("=" * 60)

# Test import nhan_su
print("\n1. Test import nhan_su:")
try:
    # Test import __init__
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "nhan_su_init",
        "addons/btl/nhan_su/__init__.py"
    )
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("   ✅ __init__.py import thành công")
    else:
        print("   ❌ Không thể load __init__.py")
except Exception as e:
    print(f"   ❌ Lỗi import __init__.py: {e}")
    import traceback
    traceback.print_exc()

# Test import models
print("\n2. Test import models:")
try:
    spec = importlib.util.spec_from_file_location(
        "nhan_su_models",
        "addons/btl/nhan_su/models/__init__.py"
    )
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("   ✅ models/__init__.py import thành công")
    else:
        print("   ❌ Không thể load models/__init__.py")
except Exception as e:
    print(f"   ❌ Lỗi import models/__init__.py: {e}")
    import traceback
    traceback.print_exc()

# Test import model class
print("\n3. Test import model class:")
try:
    spec = importlib.util.spec_from_file_location(
        "nhan_su_model",
        "addons/btl/nhan_su/models/nhan_su.py"
    )
    if spec and spec.loader:
        # Tạm thời mock odoo để test
        class MockOdoo:
            class models:
                class Model:
                    pass
            class fields:
                Char = type('Char', (), {})
                Date = type('Date', (), {})
                Selection = type('Selection', (), {})
                Boolean = type('Boolean', (), {})
                Integer = type('Integer', (), {})
                Binary = type('Binary', (), {})
            class api:
                model = lambda x: x
                depends = lambda *args: lambda x: x
        
        sys.modules['odoo'] = MockOdoo()
        sys.modules['odoo.models'] = MockOdoo.models
        sys.modules['odoo.fields'] = MockOdoo.fields
        sys.modules['odoo.api'] = MockOdoo.api
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("   ✅ nhan_su.py import thành công (với mock)")
    else:
        print("   ❌ Không thể load nhan_su.py")
except Exception as e:
    print(f"   ❌ Lỗi import nhan_su.py: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
