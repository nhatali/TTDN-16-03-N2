# Hướng Dẫn Tìm Module Trong Odoo

## Vấn đề: Không thấy module trong Apps

Nếu bạn không thấy các module `nhan_su`, `cham_cong`, `tien_luong` trong Odoo Apps, hãy làm theo các bước sau:

## Bước 1: Kiểm tra đường dẫn addons

Đảm bảo trong file config Odoo (odoo.conf) có đường dẫn đến thư mục addons:

```ini
[options]
addons_path = /home/minhtien/Business-Internship/odoo/addons,/home/minhtien/Business-Internship/addons
```

## Bước 2: Restart Odoo Server

```bash
# Dừng server hiện tại (Ctrl+C)
# Khởi động lại
python3 odoo-bin -c odoo.conf
```

## Bước 3: Update Module List

Có 2 cách:

### Cách 1: Qua giao diện Odoo
1. Vào **Apps** menu
2. Bỏ chọn filter **Apps** (chọn **All** hoặc **Extra**)
3. Click nút **Update Apps List** (góc trên bên phải)
4. Tìm kiếm: `nhan su`, `cham cong`, `tien luong`

### Cách 2: Qua command line
```bash
python3 odoo-bin -d your_database_name -u all --stop-after-init
```

Sau đó restart server và vào Apps để tìm.

## Bước 4: Cài đặt Module

1. Vào **Apps** menu
2. Tìm kiếm: `Nhân Sự`, `Chấm Công`, hoặc `Tiền Lương`
3. Click **Install** cho từng module (cài theo thứ tự: nhan_su → cham_cong → tien_luong)

## Bước 5: Kiểm tra Menu

Sau khi cài đặt, bạn sẽ thấy menu **BTL** trong menu chính với các submenu:
- **Nhân Sự**
- **Chấm Công**
- **Tiền Lương**

## Lưu ý

- Tên module trong Odoo Apps sẽ hiển thị là: **Nhân Sự**, **Chấm Công**, **Tiền Lương** (từ field `name` trong `__manifest__.py`)
- Nếu vẫn không thấy, kiểm tra log Odoo để xem có lỗi gì không
- Đảm bảo các file `__manifest__.py` và `__init__.py` đều có trong mỗi module

## Troubleshooting

Nếu vẫn không thấy module:

1. **Kiểm tra log Odoo:**
```bash
tail -f /path/to/odoo.log
```

2. **Kiểm tra syntax Python:**
```bash
python3 -m py_compile addons/btl/nhan_su/__init__.py
python3 -m py_compile addons/btl/cham_cong/__init__.py
python3 -m py_compile addons/btl/tien_luong/__init__.py
```

3. **Kiểm tra XML syntax:**
```bash
xmllint --noout addons/btl/*/views/*.xml
```

4. **Xóa cache Odoo:**
```bash
rm -rf ~/.local/share/Odoo/filestore/your_database_name/sessions/*
```
