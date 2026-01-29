# Sửa lỗi Website Module - Giải pháp cuối cùng

## Vấn đề
Website module đã được cài nhưng models chưa được tạo trong database:
- "Missing model website.visitor"
- "Missing model website"
- "Unallowed to fetch files from addon website"

## Giải pháp

### Cách 1: Upgrade Website Module (Khuyến nghị)

#### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

#### Bước 2: Upgrade Website Module
```bash
./odoo-bin -c odoo.conf -u website --stop-after-init
```

Lệnh này sẽ:
- Upgrade website module đã được cài
- Tạo các models còn thiếu
- Tạo các records cần thiết
- Dừng sau khi hoàn thành

#### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

### Cách 2: Xóa Asset Records đang reference Website

Nếu không muốn cài website, xóa các asset records:

#### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

#### Bước 2: Kết nối PostgreSQL và xóa assets
```bash
psql -h localhost -p 5431 -U odoo -d odoo -c "DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';"
```

#### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

### Cách 3: Cài đặt lại Website Module từ đầu

#### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

#### Bước 2: Gỡ cài đặt Website Module
```bash
./odoo-bin -c odoo.conf -u website --stop-after-init
# Sau đó vào Odoo UI và Uninstall website module
```

#### Bước 3: Cài đặt lại Website Module
```bash
./odoo-bin -c odoo.conf -i website --stop-after-init
```

#### Bước 4: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

## Giải thích

- **Lệnh `-i website`**: Cài đặt module mới vào database
- **Lệnh `-u website`**: Upgrade module đã được cài đặt (tạo models, records mới)
- **Vấn đề**: Website module đã được cài nhưng chưa được upgrade đầy đủ, nên models chưa được tạo
- **Giải pháp**: Upgrade website module để tạo đầy đủ models và records

## Khuyến nghị

Thử **Cách 1** trước (upgrade website module). Nếu vẫn không được, thử **Cách 2** (xóa asset records).
