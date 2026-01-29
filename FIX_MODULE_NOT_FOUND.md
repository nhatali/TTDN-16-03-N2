# Hướng Dẫn Fix Module Không Tìm Thấy

## Vấn đề
Module không hiển thị trong Apps và không tìm thấy khi search.

## Nguyên nhân có thể
1. Module chưa được Odoo load vào database
2. Có lỗi trong manifest hoặc Python code
3. Đường dẫn addons không đúng
4. Module bị đánh dấu "not installable"

## Giải pháp

### Bước 1: Kiểm tra Module Có Tồn Tại

Chạy script test:
```bash
python3 test_modules.py
```

### Bước 2: Update Module List Qua Command Line

**QUAN TRỌNG**: Phải chạy với database đúng tên:

```bash
# Kiểm tra tên database trong log Odoo khi khởi động
# Thường là 'odoo' hoặc tên bạn đã đặt

# Update module list
python3 odoo-bin -c odoo.conf -d odoo --stop-after-init

# Restart server
python3 odoo-bin -c odoo.conf
```

### Bước 3: Kiểm Tra Log Odoo

Khi khởi động Odoo, xem log có thông báo:
- `module nhan_su: not installable, skipped` → Có lỗi trong manifest
- `Some modules are not loaded` → Có lỗi dependencies
- `Missing model` → Có model cũ trong database

### Bước 4: Bật Developer Mode và Update

1. Vào **Settings** → Kéo xuống cuối → **Activate Developer Mode**
2. Vào **Settings** → **Technical** → **Database Structure** → **Modules**
3. Tìm module: `nhan_su`, `cham_cong`, `tien_luong`
4. Nếu thấy, click vào và **Upgrade** hoặc **Install**

### Bước 5: Xóa Cache và Restart

```bash
# Xóa cache Odoo
rm -rf ~/.local/share/Odoo/filestore/odoo/sessions/*

# Restart server
python3 odoo-bin -c odoo.conf
```

### Bước 6: Kiểm Tra File Manifest

Đảm bảo các file `__manifest__.py` có:
- `'installable': True`
- Không có lỗi syntax
- Dependencies đúng

### Bước 7: Nếu Vẫn Không Được

Có thể cần tạo lại module từ đầu hoặc kiểm tra:
1. Quyền truy cập file
2. Đường dẫn addons trong `odoo.conf`
3. Python version compatibility
