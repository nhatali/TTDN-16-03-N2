#!/bin/bash
# Script để upgrade module nhan_su

echo "Đang upgrade module nhan_su..."
cd /home/minhtien/Business-Internship
./odoo-bin -c odoo.conf -u nhan_su --stop-after-init

echo ""
echo "✓ Đã upgrade module nhan_su"
echo ""
echo "Bây giờ hãy:"
echo "1. Khởi động lại Odoo: ./odoo-bin -c odoo.conf"
echo "2. Clear cache trình duyệt (Ctrl+Shift+R)"
echo "3. Vào lại form nhân viên và kiểm tra tab 'Đăng ký khuôn mặt'"
