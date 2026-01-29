# Hướng Dẫn Đơn Giản - Update Module List

## Vấn đề
Script Python bị lỗi do xung đột module name. Dùng cách đơn giản hơn.

## Giải pháp đơn giản

### Cách 1: Chạy script shell (Khuyến nghị)

```bash
chmod +x update_module_simple.sh
./update_module_simple.sh
```

### Cách 2: Chạy lệnh trực tiếp

```bash
# Update module list
python3 odoo-bin -c odoo.conf -d odoo --stop-after-init

# Restart server
python3 odoo-bin -c odoo.conf
```

## Sau khi update

### Bước 1: Bật Developer Mode

1. Vào **Settings** (Thiết lập)
2. Kéo xuống cuối trang
3. Tìm **Activate Developer Mode** → Click để bật
4. Reload trang

### Bước 2: Tìm Module

Sau khi bật Developer Mode, bạn sẽ có menu mới:

**Settings** → **Technical** → **Database Structure** → **Modules**

Tại đây:
1. Tìm kiếm: `nhan_su`, `cham_cong`, `tien_luong`
2. Nếu thấy module, click vào và **Install**

### Bước 3: Hoặc tìm trong Apps

1. Vào menu **Apps**
2. Tìm kiếm: `nhan su`, `cham cong`, `tien luong`
3. Nếu thấy, click **Install**

## Nếu vẫn không thấy

Kiểm tra log Odoo khi khởi động, tìm dòng:
- `module nhan_su: not installable, skipped`
- `Some modules are not loaded`

Nếu thấy, có thể có lỗi trong manifest hoặc dependencies.

## Lưu ý

- Database name thường là `odoo` (như trong log bạn đã gửi)
- Nếu database name khác, thay `odoo` bằng tên database của bạn
- Đảm bảo Odoo server đã dừng trước khi chạy lệnh update
