# Sửa lỗi Menu không hiển thị

## Đã sửa
- Đã bỏ `groups="hr.group_hr_user"` khỏi menu items
- Menu sẽ hiển thị theo quyền của parent menu

## Cách kiểm tra

### 1. Refresh trình duyệt
- Nhấn `Ctrl+F5` hoặc `Ctrl+Shift+R` để hard refresh
- Hoặc đóng và mở lại trình duyệt

### 2. Đăng nhập lại
- Logout và login lại vào Odoo

### 3. Upgrade module
```bash
# Dừng Odoo (Ctrl+C)
./odoo-bin -c odoo.conf -u custom_hr_face_attendance --stop-after-init
# Khởi động lại
./odoo-bin -c odoo.conf
```

### 4. Kiểm tra quyền user
- Vào Settings → Users & Companies → Users
- Chọn user của bạn
- Kiểm tra Groups:
  - Phải có "Human Resources / User" hoặc "Human Resources / Manager"
  - Phải có "Attendances / User" hoặc "Attendances / Manager"

### 5. Kiểm tra menu trong Developer Mode
- Vào Settings → Activate Developer Mode
- Vào Settings → Technical → User Interface → Menu Items
- Tìm "Face Registration" và "Face Attendance"
- Kiểm tra:
  - `active` = True
  - `parent_id` đúng
  - `action_id` đúng

## Vị trí menu

Sau khi sửa, menu sẽ hiển thị ở:
- **Face Registration**: Employees → Face Registration
- **Face Attendance**: Attendances → Face Attendance

## Nếu vẫn không hiển thị

1. Kiểm tra user có quyền HR không
2. Upgrade module lại
3. Clear browser cache
4. Kiểm tra trong Developer Mode xem menu có tồn tại không
