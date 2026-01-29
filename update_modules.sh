#!/bin/bash
# Script để update module list trong Odoo

echo "Đang update module list..."

# Thay đổi tên database của bạn
DB_NAME="your_database_name"

# Chạy Odoo với lệnh update module list
python3 odoo-bin -d "$DB_NAME" -u all --stop-after-init

echo "Hoàn thành! Vui lòng restart Odoo server và kiểm tra lại."
