# Sửa lỗi Password PostgreSQL

## Vấn đề
Bạn đặt password là 123456 nhưng vẫn bị lỗi authentication.

## Nguyên nhân có thể

1. **Password trong odoo.conf khác với password trong PostgreSQL**
   - File `odoo.conf` có thể có password cũ
   - Hoặc bạn đã đổi password PostgreSQL nhưng chưa cập nhật odoo.conf

2. **PostgreSQL dùng authentication method khác**
   - Có thể dùng `trust` hoặc `peer` authentication
   - Không cần password khi kết nối local

## Giải pháp

### Cách 1: Kiểm tra password trong odoo.conf

Xem file `odoo.conf`:
```bash
cat odoo.conf | grep db_password
```

Nếu password trong file là `odoo` nhưng bạn đặt là `123456`, cần:
- Cập nhật `odoo.conf`: `db_password = 123456`
- Hoặc đổi password PostgreSQL về `odoo`

### Cách 2: Kết nối không cần password (nếu dùng trust)

Nếu PostgreSQL được cấu hình với `trust` authentication cho localhost:
```bash
psql -h localhost -p 5431 -U odoo -d odoo
```

Không cần nhập password.

### Cách 3: Reset password PostgreSQL

Nếu quên password, có thể reset:

```bash
# Kết nối với user postgres (superuser)
sudo -u postgres psql

# Hoặc nếu dùng Docker:
docker exec -it postgres_odoo-base-15-01 psql -U postgres

# Trong psql, đổi password:
ALTER USER odoo WITH PASSWORD '123456';
\q
```

Sau đó cập nhật `odoo.conf`:
```
db_password = 123456
```

### Cách 4: Dùng Odoo shell để xóa assets (không cần psql)

```bash
# Dừng Odoo trước
# Sau đó:
./odoo-bin -c odoo.conf shell -d odoo
```

Trong Python shell:
```python
# Xóa assets đang reference website
env['ir.asset'].search([('path', 'like', 'website/%')]).unlink()
env['ir.asset'].search([('path', 'like', '/website/%')]).unlink()
exit()
```

Cách này dùng password từ odoo.conf, không cần kết nối psql trực tiếp.

## Khuyến nghị

Thử **Cách 4** trước (dùng Odoo shell) - đây là cách dễ nhất và không cần biết password PostgreSQL.
