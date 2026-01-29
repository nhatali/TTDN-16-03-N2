# Giải pháp cuối cùng: Xóa Asset Records

## Nếu các cách trên không hoạt động

### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

### Bước 2: Kết nối PostgreSQL và xóa assets
```bash
psql -h localhost -p 5431 -U odoo -d odoo
```

Sau khi vào psql, chạy các lệnh sau:
```sql
-- Xem các asset đang reference website
SELECT id, name, bundle, path FROM ir_asset WHERE path LIKE '%website%' LIMIT 20;

-- Xóa các asset đang reference website
DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';

-- Thoát psql
\q
```

### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

## Hoặc dùng lệnh một dòng

```bash
PGPASSWORD=your_password psql -h localhost -p 5431 -U odoo -d odoo -c "DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';"
```

Thay `your_password` bằng password của user odoo trong PostgreSQL.

## Giải thích

- Vấn đề: Có asset records trong database đang reference website nhưng website module chưa được cài đặt đúng cách
- Giải pháp: Xóa các asset records này để Odoo không cố load chúng nữa
- Kết quả: Odoo sẽ hoạt động bình thường mà không cần website module
