# Hướng Dẫn Fix Module Không Install Được

## Vấn đề đã phát hiện

Từ log Odoo, tôi thấy:
```
WARNING odoo odoo.modules.graph: module cham_cong: not installable, skipped
WARNING odoo odoo.modules.graph: module nhan_su: not installable, skipped
```

Nguyên nhân: Đường dẫn assets trong manifest không đúng (tham chiếu đến `btl/static/` nhưng `btl` không phải là module).

## Đã sửa

✅ Đã xóa phần `assets` trong `__manifest__.py` của các module để chúng có thể install được.

## Các bước tiếp theo

### Bước 1: Restart Odoo Server

```bash
# Dừng server hiện tại (Ctrl+C trong terminal đang chạy server)
# Sau đó khởi động lại
python3 odoo-bin -c odoo.conf
```

### Bước 2: Update Module List

1. Vào Odoo → **Apps**
2. Bỏ chọn filter "Apps" (chọn **All**)
3. Click nút **Update Apps List** (góc trên bên phải, biểu tượng refresh)
4. Tìm kiếm:
   - `Nhân Sự` (hoặc `nhan su`)
   - `Chấm Công` (hoặc `cham cong`)
   - `Tiền Lương` (hoặc `tien luong`)

### Bước 3: Cài đặt Module

Cài đặt theo thứ tự:
1. **Nhân Sự** (`nhan_su`) - Cài trước
2. **Chấm Công** (`cham_cong`) - Cài sau (phụ thuộc vào nhan_su)
3. **Tiền Lương** (`tien_luong`) - Cài cuối (phụ thuộc vào cả 2 module trên)

## Lưu ý về Assets

Các file static (CSS, JS, XML) hiện đang ở `addons/btl/static/` nhưng không được load. Nếu cần sử dụng camera widget, bạn có thể:

1. **Tạm thời**: Module sẽ hoạt động nhưng camera widget có thể không hoạt động
2. **Sau này**: Di chuyển static files vào từng module hoặc tạo module `btl` riêng để chứa shared assets

## Kiểm tra sau khi cài

Sau khi cài đặt thành công, bạn sẽ thấy:
- Menu **BTL** trong menu chính
- Submenu: **Nhân Sự**, **Chấm Công**, **Tiền Lương**

## Nếu vẫn không thấy module

1. Kiểm tra log Odoo để xem có lỗi gì:
   ```bash
   # Xem log real-time
   tail -f /path/to/odoo.log
   ```

2. Kiểm tra syntax Python:
   ```bash
   python3 -m py_compile addons/btl/nhan_su/__init__.py
   python3 -m py_compile addons/btl/cham_cong/__init__.py
   python3 -m py_compile addons/btl/tien_luong/__init__.py
   ```

3. Kiểm tra XML syntax:
   ```bash
   xmllint --noout addons/btl/*/views/*.xml
   ```
