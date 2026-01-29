# Hướng Dẫn Cleanup Action Cũ Bằng SQL

## Vấn đề

Script Python bị lỗi do xung đột tên module. Dùng SQL trực tiếp để cleanup.

## Giải pháp

### Cách 1: Dùng script shell (Khuyến nghị)

```bash
chmod +x cleanup_old_actions_simple.sh
./cleanup_old_actions_simple.sh
```

### Cách 2: Chạy SQL trực tiếp

```bash
psql -U odoo -h localhost -p 5431 -d odoo
```

Sau đó chạy các lệnh SQL:

```sql
-- Vô hiệu hóa các action cũ
UPDATE ir_actions_act_window 
SET res_model = NULL 
WHERE res_model IN ('nhan_vien', 'bang_cham_cong', 'don_vi', 'chuc_vu', 'dang_ky_ca_lam_theo_ngay', 'chung_chi_bang_cap', 'dot_dang_ky', 'lich_su_cong_tac', 'danh_sach_chung_chi_bang_cap', 'don_tu');

-- Xem kết quả
SELECT COUNT(*) FROM ir_actions_act_window WHERE res_model IS NULL;

-- Thoát
\q
```

### Cách 3: Chạy SQL từ file

```bash
psql -U odoo -h localhost -p 5431 -d odoo -f cleanup_old_actions.sql
```

## Sau khi cleanup

1. **Restart Odoo server:**
   ```bash
   python3 odoo-bin -c odoo.conf
   ```

2. **Kiểm tra lại:**
   - Lỗi RPC_ERROR sẽ không còn xuất hiện
   - Có thể tìm module bình thường trong Apps

## Lưu ý

- Script sẽ vô hiệu hóa action bằng cách set `res_model = NULL`
- Không xóa action, chỉ vô hiệu hóa
- Nếu muốn xóa hoàn toàn, thay `SET res_model = NULL` bằng `DELETE FROM ir_actions_act_window WHERE ...`
