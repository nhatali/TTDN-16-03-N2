# Hướng dẫn Fix Lỗi KeyError với Model Không Tồn Tại

## Vấn đề
Lỗi `KeyError: 'nhan_vien'` hoặc `KeyError: 'bang_cham_cong'` xảy ra khi có action window trong database đang tham chiếu đến các model không còn tồn tại.

## Giải pháp đã áp dụng
Đã sửa code trong `odoo/addons/base/models/ir_actions.py` để xử lý gracefully các trường hợp model không tồn tại.

## Các bước thực hiện

### 1. Restart Odoo Server
```bash
# Dừng server hiện tại (Ctrl+C)
# Khởi động lại
python3 odoo-bin -c odoo.conf
```

### 2. Nếu vẫn còn lỗi, cleanup database

#### Cách 1: Sử dụng Odoo Shell (Khuyến nghị)
```bash
python3 odoo-bin shell -d your_database_name
```

Sau đó chạy code sau trong shell:
```python
# Lấy danh sách tất cả các model hợp lệ
valid_models = set(env.registry.keys())

# Tìm các action window có res_model không tồn tại
invalid_actions = env['ir.actions.act_window'].search([])
fixed_count = 0

for action in invalid_actions:
    if action.res_model and action.res_model not in valid_models:
        print(f"Tìm thấy action không hợp lệ: ID={action.id}, name={action.name}, res_model={action.res_model}")
        # Vô hiệu hóa action bằng cách xóa res_model
        action.write({'res_model': False})
        print(f"  -> Đã vô hiệu hóa action ID {action.id}")
        fixed_count += 1

print(f"\nTổng cộng đã fix {fixed_count} action(s)")
env.cr.commit()
```

#### Cách 2: Sử dụng SQL trực tiếp (Nếu cần)
```sql
-- Xem các action không hợp lệ
SELECT id, name, res_model 
FROM ir_actions_act_window 
WHERE res_model IN ('nhan_vien', 'bang_cham_cong');

-- Vô hiệu hóa các action này (xóa res_model)
UPDATE ir_actions_act_window 
SET res_model = NULL 
WHERE res_model IN ('nhan_vien', 'bang_cham_cong');
```

### 3. Kiểm tra lại
Sau khi cleanup, restart server và kiểm tra xem lỗi đã hết chưa.

## Lưu ý
- Code đã được sửa để tự động xử lý các model không tồn tại, nhưng cleanup database sẽ giúp loại bỏ hoàn toàn các bản ghi không hợp lệ.
- Nếu bạn muốn xóa hoàn toàn các action thay vì vô hiệu hóa, thay `action.write({'res_model': False})` bằng `action.unlink()`.
