-- Script SQL để cleanup các action window cũ tham chiếu đến model không tồn tại
-- Chạy script này trong PostgreSQL

-- Xem các action không hợp lệ
SELECT id, name, res_model 
FROM ir_actions_act_window 
WHERE res_model IN ('nhan_vien', 'bang_cham_cong', 'don_vi', 'chuc_vu', 'dang_ky_ca_lam_theo_ngay', 'chung_chi_bang_cap', 'dot_dang_ky', 'lich_su_cong_tac', 'danh_sach_chung_chi_bang_cap', 'don_tu')
   OR res_model NOT IN (
       SELECT model FROM ir_model WHERE model IS NOT NULL
   );

-- Vô hiệu hóa các action này (xóa res_model)
UPDATE ir_actions_act_window 
SET res_model = NULL 
WHERE res_model IN ('nhan_vien', 'bang_cham_cong', 'don_vi', 'chuc_vu', 'dang_ky_ca_lam_theo_ngay', 'chung_chi_bang_cap', 'dot_dang_ky', 'lich_su_cong_tac', 'danh_sach_chung_chi_bang_cap', 'don_tu')
   OR res_model NOT IN (
       SELECT model FROM ir_model WHERE model IS NOT NULL
   );

-- Hiển thị số lượng đã fix
SELECT COUNT(*) as fixed_count
FROM ir_actions_act_window 
WHERE res_model IS NULL 
  AND id IN (
      SELECT id FROM ir_actions_act_window 
      WHERE res_model IN ('nhan_vien', 'bang_cham_cong', 'don_vi', 'chuc_vu', 'dang_ky_ca_lam_theo_ngay', 'chung_chi_bang_cap', 'dot_dang_ky', 'lich_su_cong_tac', 'danh_sach_chung_chi_bang_cap', 'don_tu')
  );
