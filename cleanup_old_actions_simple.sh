#!/bin/bash
# Script đơn giản để cleanup action cũ bằng SQL

echo "=========================================="
echo "CLEANUP OLD ACTIONS - SQL"
echo "=========================================="

DB_NAME="odoo"
DB_USER="odoo"
DB_HOST="localhost"
DB_PORT="5431"

echo "Database: $DB_NAME"
echo ""

# Chạy SQL cleanup
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" <<EOF

-- Xem các action không hợp lệ trước khi fix
SELECT 'Actions cần fix:' as info;
SELECT id, name, res_model 
FROM ir_actions_act_window 
WHERE res_model IN ('nhan_vien', 'bang_cham_cong', 'don_vi', 'chuc_vu', 'dang_ky_ca_lam_theo_ngay', 'chung_chi_bang_cap', 'dot_dang_ky', 'lich_su_cong_tac', 'danh_sach_chung_chi_bang_cap', 'don_tu')
LIMIT 10;

-- Vô hiệu hóa các action này
UPDATE ir_actions_act_window 
SET res_model = NULL 
WHERE res_model IN ('nhan_vien', 'bang_cham_cong', 'don_vi', 'chuc_vu', 'dang_ky_ca_lam_theo_ngay', 'chung_chi_bang_cap', 'dot_dang_ky', 'lich_su_cong_tac', 'danh_sach_chung_chi_bang_cap', 'don_tu');

-- Hiển thị kết quả
SELECT 'Đã fix xong!' as result;
SELECT COUNT(*) as fixed_count
FROM ir_actions_act_window 
WHERE res_model IS NULL;

EOF

echo ""
echo "=========================================="
echo "Hoàn thành!"
echo "=========================================="
echo ""
echo "Bây giờ hãy restart Odoo server:"
echo "python3 odoo-bin -c odoo.conf"
echo ""
