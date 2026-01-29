# Hướng Dẫn Chi Tiết Fix Module Không Tìm Thấy

## Vấn đề
- Module không hiển thị trong Apps
- Không có nút "Update Apps List"
- Tìm kiếm module không thấy

## Giải pháp từng bước

### Bước 1: Chạy Script Force Update

```bash
# Đảm bảo đang ở thư mục Business-Internship
cd ~/Business-Internship

# Activate venv (nếu có)
source venv/bin/activate

# Chạy script
python3 force_update_modules.py
```

Script này sẽ:
- Kết nối đến database Odoo
- Force update module list
- Kiểm tra xem module có được nhận diện không

### Bước 2: Restart Odoo Server

Sau khi chạy script, restart server:

```bash
# Dừng server hiện tại (Ctrl+C)
# Khởi động lại
python3 odoo-bin -c odoo.conf
```

### Bước 3: Bật Developer Mode

1. Vào **Settings** (Thiết lập)
2. Kéo xuống cuối trang
3. Tìm **Activate Developer Mode** → Click để bật
4. Reload trang

### Bước 4: Vào Apps và Tìm Module

1. Vào menu **Apps**
2. Bây giờ sẽ có thêm menu **Settings** → **Technical** → **Modules**
3. Hoặc tìm kiếm trực tiếp: `nhan_su`, `cham_cong`, `tien_luong`

### Bước 5: Nếu Vẫn Không Thấy - Kiểm Tra Log

Khi khởi động Odoo, xem log có:
- `module nhan_su: not installable, skipped` → Có lỗi
- `Some modules are not loaded` → Có lỗi dependencies

### Bước 6: Kiểm Tra Thủ Công

Chạy lệnh này để xem module có trong database không:

```bash
# Kết nối PostgreSQL
psql -U odoo -h localhost -p 5431 -d odoo

# Chạy query
SELECT name, state, installable FROM ir_module_module WHERE name IN ('nhan_su', 'cham_cong', 'tien_luong');

# Thoát
\q
```

Nếu thấy module nhưng `installable = false`, cần sửa manifest.

## Nếu Tất Cả Đều Không Được

Có thể cần:
1. **Kiểm tra quyền file**: Đảm bảo Odoo có quyền đọc các file module
2. **Kiểm tra đường dẫn**: Đảm bảo `addons_path` trong `odoo.conf` đúng
3. **Tạo lại module**: Có thể cần tạo lại từ đầu với cấu trúc đơn giản hơn

## Liên Hệ

Nếu vẫn không được, gửi cho tôi:
- Log Odoo khi khởi động (phần có warning/error về module)
- Output của script `force_update_modules.py`
- Kết quả query database
