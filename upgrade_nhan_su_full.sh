#!/bin/bash
# Script để upgrade module nhan_su và rebuild assets

echo "=========================================="
echo "Upgrading module nhan_su..."
echo "=========================================="

cd /home/minhtien/Business-Internship

# Upgrade module
echo "1. Upgrading module nhan_su..."
./odoo-bin -c odoo.conf -u nhan_su --stop-after-init

echo ""
echo "=========================================="
echo "✓ Module đã được upgrade!"
echo "=========================================="
echo ""
echo "Bây giờ hãy:"
echo "1. Khởi động lại Odoo: ./odoo-bin -c odoo.conf"
echo "2. Clear cache trình duyệt (Ctrl+Shift+R)"
echo "3. Vào lại form nhân viên và kiểm tra field 'Ảnh'"
echo ""
echo "Nếu vẫn không thấy, thử:"
echo "- Xóa cache trình duyệt hoàn toàn"
echo "- Restart Odoo hoàn toàn (dừng và khởi động lại)"
echo "- Kiểm tra console trình duyệt (F12) xem có lỗi JavaScript không"
