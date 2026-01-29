#!/bin/bash
# Script đơn giản để update module list

echo "=========================================="
echo "UPDATE MODULE LIST"
echo "=========================================="

# Đọc database name từ config hoặc dùng mặc định
DB_NAME="odoo"

echo "Database: $DB_NAME"
echo ""
echo "Đang update module list..."
echo ""

# Chạy Odoo với --stop-after-init để update module list
python3 odoo-bin -c odoo.conf -d "$DB_NAME" --stop-after-init

echo ""
echo "=========================================="
echo "Hoàn thành!"
echo "=========================================="
echo ""
echo "Bây giờ hãy:"
echo "1. Restart Odoo server: python3 odoo-bin -c odoo.conf"
echo "2. Vào Odoo → Apps → Tìm kiếm module"
echo "3. Hoặc bật Developer Mode → Settings → Technical → Modules"
echo ""
