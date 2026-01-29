# Sửa lỗi Menu không hiển thị - Hướng dẫn cuối cùng

## Đã sửa
- Đã thêm `groups="hr.group_hr_user"` vào menu Face Registration
- Đã thêm `groups="hr_attendance.group_hr_attendance_user"` vào menu Face Attendance

## Kiểm tra Menu trong Database

Chạy script để kiểm tra:
```bash
python3 check_menu.py
```

Script sẽ hiển thị:
- Menu có tồn tại trong database không
- Parent menu có đúng không
- Action có tồn tại không

## Kiểm tra Quyền User

### 1. Vào Settings → Users & Companies → Users
- Chọn user của bạn
- Kiểm tra tab "Access Rights"

### 2. Kiểm tra Groups
User phải có ít nhất một trong các groups sau:
- **Human Resources / User** (`hr.group_hr_user`)
- **Human Resources / Manager** (`hr.group_hr_manager`)
- **Attendances / User** (`hr_attendance.group_hr_attendance_user`)

### 3. Nếu chưa có quyền
- Tích vào group "Human Resources / User"
- Tích vào group "Attendances / User"
- Lưu và đăng nhập lại

## Upgrade Module

Sau khi sửa groups, upgrade module:
```bash
# Dừng Odoo (Ctrl+C)
./odoo-bin -c odoo.conf -u custom_hr_face_attendance --stop-after-init
# Khởi động lại
./odoo-bin -c odoo.conf
```

## Kiểm tra trong Developer Mode

1. Vào Settings → Activate Developer Mode
2. Vào Settings → Technical → User Interface → Menu Items
3. Tìm "Face Registration" và "Face Attendance"
4. Kiểm tra:
   - `active` = True
   - `parent_id` đúng
   - `action_id` đúng
   - `groups_id` có groups phù hợp

## Vị trí Menu

Sau khi có quyền, menu sẽ hiển thị ở:
- **Face Registration**: Employees → Face Registration
- **Face Attendance**: Attendances → Face Attendance

## Nếu vẫn không hiển thị

1. Chạy script `check_menu.py` để kiểm tra menu trong database
2. Kiểm tra quyền user
3. Upgrade module lại
4. Clear browser cache và đăng nhập lại
