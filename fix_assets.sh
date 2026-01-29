#!/bin/bash
# Script để xóa asset records đang reference website

echo "Đang kết nối PostgreSQL..."
echo "Nhập password của user odoo khi được yêu cầu:"

psql -h localhost -p 5431 -U odoo -d odoo << EOF
-- Xem các asset đang reference website
SELECT id, name, bundle, path FROM ir_asset WHERE path LIKE '%website%' LIMIT 20;

-- Xóa các asset đang reference website
DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';

-- Xác nhận đã xóa
SELECT COUNT(*) as remaining_website_assets FROM ir_asset WHERE path LIKE '%website%';
EOF

echo "Đã xóa xong! Khởi động lại Odoo:"
echo "./odoo-bin -c odoo.conf"
