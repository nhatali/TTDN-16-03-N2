# Giải thích và Sửa lỗi

## Tại sao lúc đầu không cần xóa gì mà vẫn chạy được?

### Lúc đầu (trước khi tôi tạo patches):
- **Không có asset records nào** trong database đang reference website
- Odoo chạy bình thường vì không có gì cố load website assets
- Module `custom_hr_face_attendance` hoạt động độc lập, không cần website

### Sau khi tôi tạo patches và cài website:
- **Có asset records được tạo** trong database đang reference website
- Có thể do:
  1. Khi cài website module (`-i website`), nó tạo asset records
  2. Hoặc có module khác đã tạo asset records reference website
  3. Hoặc khi upgrade, có asset records mới được tạo

### Vấn đề hiện tại:
- Có asset records trong database đang reference website
- Nhưng website module chưa được cài đặt đúng cách (models chưa được tạo)
- Odoo cố load các assets này → Lỗi "Unallowed to fetch files from addon website"

## Giải pháp

### Cách 1: Dùng password đúng từ odoo.conf

Password trong `odoo.conf` là `odoo`:

```bash
PGPASSWORD=odoo psql -h localhost -p 5431 -U odoo -d odoo -c "DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';"
```

### Cách 2: Uninstall Website Module hoàn toàn (Không cần xóa thủ công)

#### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

#### Bước 2: Uninstall Website Module
```bash
./odoo-bin -c odoo.conf shell -d odoo
```

Trong shell, chạy:
```python
env['ir.module.module'].search([('name', '=', 'website')]).button_immediate_uninstall()
exit()
```

#### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

### Cách 3: Kết nối PostgreSQL trực tiếp

```bash
psql -h localhost -p 5431 -U odoo -d odoo
```

Khi được hỏi password, nhập: `odoo`

Sau đó chạy:
```sql
DELETE FROM ir_asset WHERE path LIKE 'website/%' OR path LIKE '/website/%';
\q
```

## Khuyến nghị

Thử **Cách 1** trước với password `odoo`. Nếu không được, thử **Cách 2** (uninstall website module).
