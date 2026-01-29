# Hướng dẫn Sửa lỗi Website

## Vấn đề
Odoo không thể truy cập được vì lỗi "Unallowed to fetch files from addon website" và "KeyError: 'website'"

## Giải pháp

### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C` trong terminal

### Bước 2: Xóa Python Cache
```bash
find addons/custom_hr_face_attendance -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
find addons/custom_hr_face_attendance -name "*.pyc" -delete 2>/dev/null || true
```

### Bước 3: Upgrade Module (QUAN TRỌNG!)
```bash
./odoo-bin -c odoo.conf -u custom_hr_face_attendance --stop-after-init
```

### Bước 4: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

## Nếu vẫn không được

### Option 1: Cài đặt Website Module (Khuyến nghị)
```bash
# Trong Odoo UI: Apps → Tìm "Website" → Install
# Hoặc qua command line:
./odoo-bin -c odoo.conf -i website --stop-after-init
```

### Option 2: Tắt module đang gây lỗi
Nếu có module khác đang reference website, tắt nó tạm thời:
- Vào Apps → Tìm module có dependency website → Uninstall

## Giải thích
Module `custom_hr_face_attendance` đã có patches để xử lý trường hợp website chưa được cài đặt, nhưng cần upgrade module để patches được load vào Odoo.
