# Hướng Dẫn Chạy Lệnh Update Module List

## Bước 1: Đảm bảo bạn đang ở đúng thư mục

```bash
cd ~/Business-Internship
```

## Bước 2: Chạy lệnh update module list

Có 2 cách:

### Cách 1: Chạy script (Khuyến nghị)

```bash
chmod +x update_module_list.sh
./update_module_list.sh
```

Script sẽ hỏi tên database của bạn, nhập vào và Enter.

### Cách 2: Chạy lệnh trực tiếp

```bash
# Thay 'your_database_name' bằng tên database thực tế của bạn
python3 odoo-bin -c odoo.conf -d your_database_name --stop-after-init
```

**Lưu ý:** 
- `your_database_name` là tên database Odoo của bạn (thường là tên bạn đã tạo khi cài đặt Odoo)
- Lệnh này sẽ dừng server sau khi update xong

## Bước 3: Restart Odoo Server

Sau khi chạy lệnh update, restart server:

```bash
python3 odoo-bin -c odoo.conf
```

## Bước 4: Vào Odoo và tìm module

1. Mở trình duyệt, vào Odoo (thường là http://localhost:8069)
2. Vào menu **Apps**
3. Bỏ chọn filter "Apps" (chọn "All" hoặc "Extra")
4. Click nút **Update Apps List** (góc trên bên phải, biểu tượng refresh)
5. Tìm kiếm:
   - `Nhân Sự` (hoặc `nhan su`)
   - `Chấm Công` (hoặc `cham cong`)
   - `Tiền Lương` (hoặc `tien luong`)

## Bước 5: Cài đặt module

Cài đặt theo thứ tự:
1. **Nhân Sự** (nhan_su) - Cài trước
2. **Chấm Công** (cham_cong) - Cài sau
3. **Tiền Lương** (tien_luong) - Cài cuối

## Troubleshooting

### Nếu không biết tên database:

```bash
# Xem danh sách database
psql -U odoo -h localhost -p 5431 -l
```

Hoặc kiểm tra trong file config hoặc log Odoo.

### Nếu gặp lỗi permission:

```bash
chmod +x update_module_list.sh
```

### Nếu vẫn không thấy module:

1. Kiểm tra log Odoo để xem có lỗi gì không
2. Đảm bảo đường dẫn addons trong `odoo.conf` đúng:
   ```ini
   addons_path = addons
   ```
3. Kiểm tra các file `__manifest__.py` và `__init__.py` có đầy đủ không
