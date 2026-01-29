#!/bin/bash
# Script để force upgrade module nhan_su và clear cache

echo "=========================================="
echo "Force Upgrading module nhan_su..."
echo "=========================================="

cd /home/minhtien/Business-Internship

# Stop Odoo if running
echo "1. Stopping Odoo (if running)..."
pkill -f "odoo-bin" || true
sleep 2

# Upgrade module với --init để force reload
echo "2. Upgrading module nhan_su (force)..."
./odoo-bin -c odoo.conf -u nhan_su --stop-after-init

echo ""
echo "=========================================="
echo "✓ Module đã được upgrade!"
echo "=========================================="
echo ""
echo "Bây giờ hãy:"
echo "1. Khởi động lại Odoo: ./odoo-bin -c odoo.conf"
echo "2. Mở trình duyệt và vào Odoo"
echo "3. Nhấn F12 để mở Developer Tools"
echo "4. Vào tab 'Application' → 'Clear storage' → 'Clear site data'"
echo "5. Hoặc nhấn Ctrl+Shift+R để hard refresh"
echo "6. Vào lại form nhân viên và kiểm tra field 'Ảnh'"
echo ""
echo "Nếu vẫn không thấy widget:"
echo "- Kiểm tra console (F12) xem có lỗi JavaScript không"
echo "- Kiểm tra Network tab xem file face_image_widget.js có được load không"
