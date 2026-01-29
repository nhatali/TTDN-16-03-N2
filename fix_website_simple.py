#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đơn giản để xóa asset records - Cách 2
"""

import psycopg2
import sys

# Thông tin kết nối từ odoo.conf
DB_HOST = 'localhost'
DB_PORT = 5431
DB_USER = 'odoo'
DB_NAME = 'odoo'
# Thử các password phổ biến
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

def fix_assets():
    # Thử kết nối với các password
    conn, used_password = try_connect()
    if not conn:
        print("✗ Không thể kết nối PostgreSQL với các password: odoo, 123456, postgres")
        print("  Vui lòng sửa password trong file fix_website_simple.py")
        return False
    
    print(f"✓ Đã kết nối với password: {'(empty)' if not used_password else used_password}")
    
    try:
        
        cur = conn.cursor()
        
        # Đếm số assets
        cur.execute("""
            SELECT COUNT(*) FROM ir_asset 
            WHERE path LIKE 'website/%' OR path LIKE '/website/%'
        """)
        count = cur.fetchone()[0]
        
        if count == 0:
            print("✓ Không có asset nào đang reference website")
            cur.close()
            conn.close()
            return True
        
        print(f"Tìm thấy {count} asset(s) đang reference website")
        
        # Xóa assets
        cur.execute("""
            DELETE FROM ir_asset 
            WHERE path LIKE 'website/%' OR path LIKE '/website/%'
        """)
        
        conn.commit()
        print(f"✓ Đã xóa {count} asset(s)")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        if conn:
            conn.close()
        return False

if __name__ == '__main__':
    print("Đang xóa asset records đang reference website...")
    if fix_assets():
        print("\n✓ Hoàn thành! Khởi động lại Odoo:")
        print("  ./odoo-bin -c odoo.conf")
    else:
        print("\n✗ Có lỗi xảy ra")
        sys.exit(1)
