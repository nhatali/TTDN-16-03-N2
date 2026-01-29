#!/bin/bash
# Script để update module list trong Odoo

echo "=========================================="
echo "Update Module List trong Odoo"
echo "=========================================="

# Đọc tên database từ config hoặc yêu cầu người dùng nhập
read -p "Nhập tên database của bạn (hoặc Enter để dùng 'odoo'): " DB_NAME
DB_NAME=${DB_NAME:-odoo}

echo ""
echo "Đang update module list cho database: $DB_NAME"
echo "Lưu ý: Server sẽ dừng sau khi update xong"
echo ""

# Chạy Odoo với lệnh update module list
python3 odoo-bin -c odoo.conf -d "$DB_NAME" --stop-after-init

echo ""
echo "=========================================="
echo "Hoàn thành!"
echo "=========================================="
echo "Bây giờ bạn cần:"
echo "1. Restart Odoo server: python3 odoo-bin -c odoo.conf"
echo "2. Vào Odoo → Apps → Tìm kiếm: 'Nhân Sự', 'Chấm Công', 'Tiền Lương'"
echo "3. Cài đặt các module theo thứ tự: nhan_su → cham_cong → tien_luong"
