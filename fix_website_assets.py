#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để xóa asset records đang reference website
Chạy script này để tự động sửa lỗi
"""

import sys
import os

# Thêm đường dẫn Odoo vào sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'odoo'))

import odoo
from odoo import api, SUPERUSER_ID

def fix_website_assets():
    """Xóa asset records đang reference website"""
    
    # Khởi tạo Odoo
    odoo.tools.config.parse_config(['-c', 'odoo.conf'])
    
    # Kết nối database
    db_name = odoo.tools.config['db_name']
    if not db_name:
        print("ERROR: Không tìm thấy database name trong config")
        return False
    
    registry = odoo.registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Tìm các asset đang reference website
        assets = env['ir.asset'].search([
            '|',
            ('path', 'like', 'website/%'),
            ('path', 'like', '/website/%')
        ])
        
        if not assets:
            print("✓ Không có asset nào đang reference website")
            return True
        
        print(f"Tìm thấy {len(assets)} asset(s) đang reference website:")
        for asset in assets:
            print(f"  - {asset.name}: {asset.path}")
        
        # Xóa các assets
        asset_ids = assets.ids
        env['ir.asset'].browse(asset_ids).unlink()
        cr.commit()
        
        print(f"✓ Đã xóa {len(asset_ids)} asset(s)")
        return True

if __name__ == '__main__':
    try:
        print("Đang xóa asset records đang reference website...")
        success = fix_website_assets()
        if success:
            print("\n✓ Hoàn thành! Khởi động lại Odoo:")
            print("  ./odoo-bin -c odoo.conf")
        else:
            print("\n✗ Có lỗi xảy ra")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
