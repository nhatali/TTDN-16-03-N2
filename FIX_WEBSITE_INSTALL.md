# Sửa lỗi: Cài đặt Website Module vào Database

## Vấn đề
- Lỗi: "Unallowed to fetch files from addon website"
- Nguyên nhân: Có asset trong database đang reference website, nhưng website module chưa được cài đặt vào database
- Lệnh `-i website` chỉ cài vào filesystem, không cài vào database

## Giải pháp

### Cách 1: Cài đặt Website Module vào Database (Khuyến nghị)

#### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

#### Bước 2: Cài đặt Website Module vào Database
```bash
./odoo-bin -c odoo.conf -i website --stop-after-init
```

Lệnh này sẽ:
- Cài đặt website module vào database
- Tạo các models: website, website.visitor, website.page, etc.
- Tạo các asset records cần thiết
- Dừng sau khi hoàn thành

#### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

### Cách 2: Xóa Asset Records đang reference Website (Nếu không muốn cài website)

Nếu bạn không muốn cài website module, có thể xóa các asset records:

#### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

#### Bước 2: Kết nối PostgreSQL và xóa assets
```bash
psql -h localhost -p 5431 -U odoo -d odoo -c "DELETE FROM ir_asset WHERE path LIKE 'website/%';"
```

#### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

## Giải thích

- **Lệnh `-i website`**: Cài đặt module vào database (tạo models, records, etc.)
- **Lệnh `-u website`**: Upgrade module đã được cài đặt
- **Vấn đề**: Có asset records trong database đang reference website nhưng website chưa được cài đặt
- **Giải pháp**: Cài đặt website module vào database để tạo các models và records cần thiết

## Lưu ý

Sau khi cài đặt website module, Odoo sẽ hoạt động bình thường. Module `custom_hr_face_attendance` sẽ hoạt động mà không cần website module (chỉ cần khi dùng public endpoints).
