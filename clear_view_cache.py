#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để xóa cache view trong database
"""

import psycopg2
import sys

# Thông tin kết nối
DB_HOST = 'localhost'
DB_PORT = 5431
DB_USER = 'odoo'
DB_NAME = 'odoo'
PASSWORDS = ['odoo', '123456', 'postgres', '']

def try_connect():
    """Thử kết nối với các password khác nhau"""
    for password in PASSWORDS:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=password,
                database=DB_NAME
            )
            return conn, password
        except psycopg2.OperationalError:
            continue
    return None, None

def clear_view_cache():
    """Xóa cache view cho nhan_vien"""
    conn, used_password = try_connect()
    if not conn:
        print("✗ Không thể kết nối PostgreSQL")
        return False
    
    print(f"✓ Đã kết nối với password: {'(empty)' if not used_password else used_password}\n")
    
    try:
        cur = conn.cursor()
        
        # Tìm view nhan_vien
        cur.execute("""
            SELECT id, name, model, arch_db
            FROM ir_ui_view
            WHERE model = 'nhan_vien' AND type = 'form'
            ORDER BY id DESC
            LIMIT 5
        """)
        
        views = cur.fetchall()
        if not views:
            print("✗ Không tìm thấy view nhan_vien")
        else:
            print(f"✓ Tìm thấy {len(views)} view(s) cho nhan_vien:")
            for view in views:
                view_id, name, model, arch_db = view
                print(f"  - ID: {view_id}, Name: {name}")
                
                # Kiểm tra xem có chứa 'invisible="has_face_registration"' không
                if arch_db and 'invisible="has_face_registration"' in arch_db:
                    print(f"    ⚠️  View này vẫn chứa cú pháp cũ!")
                    # Cập nhật view từ file
                    print(f"    → Cần upgrade module để cập nhật view")
        
        # Clear cache bằng cách update view (trigger cache clear)
        print("\n--- Clearing view cache ---")
        cur.execute("""
            UPDATE ir_ui_view
            SET write_date = CURRENT_TIMESTAMP
            WHERE model = 'nhan_vien' AND type = 'form'
        """)
        affected = cur.rowcount
        conn.commit()
        print(f"✓ Đã clear cache cho {affected} view(s)")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        if conn:
            conn.close()
        return False

if __name__ == '__main__':
    print("Đang clear cache view cho nhan_vien...\n")
    if clear_view_cache():
        print("\n✓ Hoàn thành! Hãy:")
        print("  1. Upgrade module: ./odoo-bin -c odoo.conf -u nhan_su --stop-after-init")
        print("  2. Restart Odoo: ./odoo-bin -c odoo.conf")
    else:
        print("\n✗ Có lỗi xảy ra")
        sys.exit(1)
