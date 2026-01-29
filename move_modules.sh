#!/bin/bash
# Script để di chuyển module ra ngoài thư mục btl

echo "=========================================="
echo "DI CHUYỂN MODULE RA NGOÀI THƯ MỤC BTL"
echo "=========================================="

cd ~/Business-Internship/addons

# Backup thư mục btl (tùy chọn)
# cp -r btl btl_backup

# Di chuyển các module
echo "Đang di chuyển nhan_su..."
mv btl/nhan_su .

echo "Đang di chuyển cham_cong..."
mv btl/cham_cong .

echo "Đang di chuyển tien_luong..."
mv btl/tien_luong .

echo ""
echo "=========================================="
echo "Hoàn thành!"
echo "=========================================="
echo ""
echo "Các module đã được di chuyển:"
echo "  - addons/nhan_su/"
echo "  - addons/cham_cong/"
echo "  - addons/tien_luong/"
echo ""
echo "Bây giờ hãy:"
echo "1. Update module list: python3 odoo-bin -c odoo.conf -d odoo --stop-after-init"
echo "2. Restart server: python3 odoo-bin -c odoo.conf"
echo "3. Vào Apps và tìm module"
echo ""
