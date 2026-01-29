#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để kiểm tra menu trong database
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

def check_menu():
    conn, used_password = try_connect()
    if not conn:
        print("✗ Không thể kết nối PostgreSQL")
        return False
    
    print(f"✓ Đã kết nối với password: {'(empty)' if not used_password else used_password}\n")
    
    try:
        cur = conn.cursor()
        
        # Kiểm tra menu Face Registration
        cur.execute("""
            SELECT id, name, parent_id, action, active, sequence
            FROM ir_ui_menu
            WHERE name LIKE '%Face%'
            ORDER BY id
        """)
        
        menus = cur.fetchall()
        if not menus:
            print("✗ Không tìm thấy menu Face Registration trong database")
            print("  Có thể module chưa được cài đặt đúng cách")
            print("  Hãy upgrade module: ./odoo-bin -c odoo.conf -u custom_hr_face_attendance --stop-after-init")
        else:
            print(f"✓ Tìm thấy {len(menus)} menu(s):")
            for menu in menus:
                menu_id, name, parent_id, action, active, sequence = menu
                action_str = f"Action ID: {action}" if action else "No Action"
                print(f"  - ID: {menu_id}, Name: {name}, Active: {active}, Sequence: {sequence}")
                print(f"    Parent ID: {parent_id}, {action_str}")
        
        # Kiểm tra parent menu
        print("\n--- Kiểm tra Parent Menu ---")
        cur.execute("""
            SELECT id, name, complete_name
            FROM ir_ui_menu
            WHERE id IN (
                SELECT DISTINCT parent_id FROM ir_ui_menu WHERE name LIKE '%Face%'
            )
        """)
        parents = cur.fetchall()
        if parents:
            for parent in parents:
                print(f"  - Parent: {parent[1]} (ID: {parent[0]})")
        else:
            print("  ✗ Không tìm thấy parent menu")
        
        # Kiểm tra action
        print("\n--- Kiểm tra Action ---")
        cur.execute("""
            SELECT id, name, res_model, type
            FROM ir_actions_act_window
            WHERE name LIKE '%Face%'
        """)
        actions = cur.fetchall()
        if actions:
            for action in actions:
                print(f"  - Action: {action[1]} (ID: {action[0]}, Model: {action[2]})")
        else:
            print("  ✗ Không tìm thấy action")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        if conn:
            conn.close()
        return False

if __name__ == '__main__':
    print("Đang kiểm tra menu trong database...\n")
    check_menu()
