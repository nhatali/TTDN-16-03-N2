# Khôi phục Odoo về trạng thái hoạt động

## Đã làm
✅ Đã xóa các patches gây xung đột (ir_asset, ir_http, ir_ui_view)
✅ Module `custom_hr_face_attendance` đã được khôi phục về trạng thái ban đầu

## Vấn đề hiện tại
Website module đã được cài nhưng chưa được cài đặt vào database (vẫn có lỗi "Missing model website")

## Giải pháp

### Bước 1: Dừng Odoo Server
Nhấn `Ctrl+C`

### Bước 2: Upgrade Website Module vào Database
```bash
./odoo-bin -c odoo.conf -u website --stop-after-init
```

Lệnh này sẽ:
- Cài đặt website module vào database
- Tạo các models cần thiết (website, website.visitor, website.page, etc.)
- Dừng sau khi hoàn thành

### Bước 3: Khởi động lại Odoo
```bash
./odoo-bin -c odoo.conf
```

### Bước 4: Upgrade Module custom_hr_face_attendance
Sau khi Odoo chạy được, upgrade module của bạn:
```bash
./odoo-bin -c odoo.conf -u custom_hr_face_attendance --stop-after-init
```

Sau đó khởi động lại:
```bash
./odoo-bin -c odoo.conf
```

## Giải thích
- Lệnh `-i website` chỉ cài module vào filesystem
- Lệnh `-u website` mới cài đặt vào database và tạo các models
- Module `custom_hr_face_attendance` đã được khôi phục về trạng thái ban đầu, không còn patches gây xung đột
