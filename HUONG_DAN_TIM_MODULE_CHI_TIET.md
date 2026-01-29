# Hướng Dẫn Tìm Module Chi Tiết

## Nếu không thấy module trong Apps

### Bước 1: Kiểm tra module có trong database không

Chạy script kiểm tra:

```bash
python3 check_modules_in_db.py
```

Script này sẽ cho biết:
- Module có tồn tại trong database không
- State của module (uninstalled, installed, etc.)
- Module có installable không

### Bước 2: Bật Developer Mode

1. Vào **Settings** (Thiết lập)
2. Kéo xuống cuối → **Activate Developer Mode** (Bật Chế Độ Nhà Phát Triển)
3. Reload trang

### Bước 3: Tìm trong Technical Menu

Sau khi bật Developer Mode:

1. Vào **Settings** → **Technical** → **Database Structure** → **Modules**
2. Tìm kiếm: `nhan_su`, `cham_cong`, `tien_luong`
3. Nếu thấy module với state="uninstalled", click vào và **Install**

### Bước 4: Hoặc tìm trong Apps với filter đúng

1. Vào **Apps**
2. **Bỏ chọn tất cả filter** (chọn "All" hoặc "Extra")
3. Tìm kiếm: `nhan_su`, `cham_cong`, `tien_luong` (dùng underscore, không dùng space)
4. Hoặc tìm: `nhan su`, `cham cong`, `tien luong` (dùng space)

### Bước 5: Nếu vẫn không thấy - Force update lại

```bash
# Update lại module list
python3 odoo-bin -c odoo.conf -d odoo --stop-after-init

# Restart server
python3 odoo-bin -c odoo.conf
```

### Bước 6: Kiểm tra module có tồn tại ở đúng vị trí không

```bash
# Kiểm tra file manifest
ls -la addons/nhan_su/__manifest__.py
ls -la addons/cham_cong/__manifest__.py
ls -la addons/tien_luong/__manifest__.py
```

Nếu không thấy file, module chưa được di chuyển đúng cách.

## Lưu ý

- Module phải nằm trực tiếp trong `addons/`, không nằm trong subfolder
- Sau khi di chuyển, phải update module list lại
- Có thể cần restart server sau khi update
