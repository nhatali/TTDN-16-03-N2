# Hướng dẫn Test Module nhanh (Không cần menu)

## Cách 1: Test qua Employee Form (Dễ nhất)

1. **Vào Employees** → Chọn một employee bất kỳ
2. **Trong form employee**, tìm:
   - Button **"Register Face"** (ở header)
   - Smart button **"Face Registrations"** (ở button box)
   - Tab **"Face Registration"** (ở notebook)

3. **Click button "Register Face"** → Mở wizard đăng ký face
4. **Upload ảnh** và đăng ký

## Cách 2: Truy cập trực tiếp qua URL

### Test Face Registration List
```
http://localhost:8069/web#action=custom_hr_face_attendance.action_face_registration&model=face.registration&view_type=list
```

### Test Face Attendance List
```
http://localhost:8069/web#action=custom_hr_face_attendance.action_face_attendance&model=hr.attendance&view_type=list
```

Copy URL trên và paste vào trình duyệt.

## Cách 3: Tìm trong Apps

1. Vào **Apps**
2. Tìm "Custom HR Face Attendance"
3. Click vào module
4. Click button **"Open"** hoặc **"Execute"** (nếu có)

## Cách 4: Test API Endpoints

### Test Face Check-in (Public)
```
http://localhost:8069/face_attendance/checkin
```

### Test Face Check-out (Public)
```
http://localhost:8069/face_attendance/checkout
```

## Kiểm tra Module hoạt động

### 1. Kiểm tra Model tồn tại
- Vào Developer Mode
- Settings → Technical → Database Structure → Models
- Tìm "face.registration" → Phải có

### 2. Kiểm tra Button trên Employee
- Vào một employee
- Kiểm tra có button "Register Face" không
- Nếu không có, có thể do:
  - User không có quyền `hr.group_hr_user`
  - Module chưa được upgrade

### 3. Test Wizard
- Click button "Register Face"
- Wizard phải mở ra
- Upload ảnh và test

## Nếu vẫn không test được

1. **Kiểm tra quyền user:**
   - Settings → Users → Chọn user
   - Tích vào "Human Resources / User"

2. **Upgrade module:**
   ```bash
   ./odoo-bin -c odoo.conf -u custom_hr_face_attendance --stop-after-init
   ```

3. **Refresh trình duyệt:**
   - Ctrl+F5 hoặc đăng nhập lại
