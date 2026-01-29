# Hướng Dẫn Sau Khi Update Module List

## ⚠️ Vấn đề phát hiện

Từ log, tôi thấy module bị đánh dấu **"not installable"**:
- `module cham_cong: not installable, skipped`
- `module nhan_su: not installable, skipped`

Điều này có nghĩa là có lỗi trong code khiến Odoo không thể load module.

## 🔧 Các bước tiếp theo

### Bước 1: Kiểm tra lỗi trong code

Chạy lệnh này để kiểm tra syntax:

```bash
# Kiểm tra nhan_su
python3 -m py_compile addons/btl/nhan_su/__init__.py
python3 -m py_compile addons/btl/nhan_su/models/__init__.py
python3 -m py_compile addons/btl/nhan_su/models/nhan_su.py

# Kiểm tra cham_cong
python3 -m py_compile addons/btl/cham_cong/__init__.py
python3 -m py_compile addons/btl/cham_cong/models/__init__.py
python3 -m py_compile addons/btl/cham_cong/models/cham_cong.py
```

Nếu có lỗi, sẽ hiển thị ngay.

### Bước 2: Kiểm tra XML files

```bash
# Kiểm tra XML syntax
xmllint --noout addons/btl/nhan_su/views/*.xml
xmllint --noout addons/btl/cham_cong/views/*.xml
```

### Bước 3: Restart Odoo và xem log chi tiết

```bash
# Restart server và xem log
python3 odoo-bin -c odoo.conf 2>&1 | grep -i "nhan_su\|cham_cong\|error\|warning"
```

### Bước 4: Bật Developer Mode và kiểm tra

1. Vào **Settings** (Thiết lập)
2. Kéo xuống cuối → **Activate Developer Mode** (Bật Chế Độ Nhà Phát Triển)
3. Reload trang

### Bước 5: Tìm Module trong Technical Menu

Sau khi bật Developer Mode:

1. Vào **Settings** (Thiết lập)
2. Vào **Technical** (Kỹ Thuật)
3. Vào **Database Structure** (Cấu Trúc Cơ Sở Dữ Liệu)
4. Vào **Modules** (Mô Đun)
5. Tìm kiếm: `nhan_su`, `cham_cong`, `tien_luong`

Nếu thấy module nhưng có dấu cảnh báo, click vào để xem lỗi chi tiết.

### Bước 6: Hoặc tìm trong Apps

1. Vào menu **Apps** (Ứng Dụng)
2. Tìm kiếm: `nhan su`, `cham cong`, `tien luong`
3. Nếu thấy, click **Install** (Cài Đặt)

## 🔍 Nếu vẫn không thấy

Gửi cho tôi:
1. Output của các lệnh kiểm tra syntax ở trên
2. Log Odoo khi khởi động (phần có ERROR hoặc WARNING về module)
3. Screenshot nếu có thể

## 💡 Lưu ý

Module bị "not installable" thường do:
- Lỗi syntax trong Python code
- Lỗi trong XML files
- Dependencies không đúng
- Thiếu file bắt buộc

Tôi sẽ giúp bạn fix từng lỗi một khi có thông tin chi tiết.
