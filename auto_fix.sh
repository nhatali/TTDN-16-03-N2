#!/bin/bash
# Script tự động sửa lỗi website assets

echo "=========================================="
echo "Tự động sửa lỗi Website Assets"
echo "=========================================="
echo ""

# Thử với password odoo trước
echo "Đang thử kết nối với password 'odoo'..."
PGPASSWORD=odoo psql -h localhost -p 5431 -U odoo -d odoo -c "DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Đã xóa assets thành công với password 'odoo'"
    exit 0
fi

# Nếu không được, thử với password 123456
echo "Đang thử kết nối với password '123456'..."
PGPASSWORD=123456 psql -h localhost -p 5431 -U odoo -d odoo -c "DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Đã xóa assets thành công với password '123456'"
    exit 0
fi

# Nếu vẫn không được, hướng dẫn thủ công
echo "✗ Không thể kết nối tự động"
echo ""
echo "Vui lòng chạy lệnh sau với password đúng:"
echo "  PGPASSWORD=<password> psql -h localhost -p 5431 -U odoo -d odoo -c \"DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';\""
echo ""
echo "Hoặc chạy script Python:"
echo "  python3 fix_website_simple.py"
exit 1
