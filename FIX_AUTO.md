# Tự động Sửa lỗi - Script Python

## Xin lỗi vì đã gây ra vấn đề

Tôi đã tạo ra vấn đề khi cài website module, và giờ tạo script để tự động sửa.

## Cách sử dụng

### Cách 1: Script đơn giản (Khuyến nghị)

#### Bước 1: Sửa password trong script (nếu cần)
Mở file `fix_website_simple.py` và sửa dòng:
```python
DB_PASSWORD = 'odoo'  # Thay đổi nếu password khác
```

Nếu password của bạn là `123456`, sửa thành:
```python
DB_PASSWORD = '123456'
```

#### Bước 2: Chạy script
```bash
python3 fix_website_simple.py
```

Script sẽ tự động:
- Kết nối PostgreSQL
- Tìm và xóa các asset đang reference website
- Báo cáo kết quả

#### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

### Cách 2: Script dùng Odoo ORM

```bash
python3 fix_website_assets.py
```

Script này dùng Odoo ORM, tự động lấy thông tin từ `odoo.conf`.

## Giải thích

- **Vấn đề**: Khi cài website module, các asset records được tạo trong database
- **Giải pháp**: Xóa các asset records này
- **Script**: Tự động làm việc này, không cần nhập lệnh thủ công

## Nếu vẫn lỗi

Gửi log lỗi để tôi kiểm tra thêm.
