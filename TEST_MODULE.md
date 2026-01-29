# Hướng dẫn Test Module custom_hr_face_attendance

## Cách 1: Truy cập trực tiếp qua URL (Không cần menu)

### Test Face Registration
```
http://localhost:8069/web#action=custom_hr_face_attendance.action_face_registration&model=face.registration&view_type=list
```

### Test Face Attendance
```
http://localhost:8069/web#action=custom_hr_face_attendance.action_face_attendance&model=hr.attendance&view_type=list
```

## Cách 2: Test qua Employee Form

1. Vào **Employees** → Chọn một employee
2. Trong form employee, tìm button **"Register Face"** hoặc **"Face Registration"**
3. Click button để mở wizard đăng ký face

## Cách 3: Kiểm tra Menu trong Developer Mode

1. Vào **Settings** → **Activate Developer Mode**
2. Vào **Settings** → **Technical** → **User Interface** → **Menu Items**
3. Tìm "Face Registration" và "Face Attendance"
4. Kiểm tra:
   - `active` = True
   - `parent_id` đúng
   - `action_id` đúng

Nếu menu có nhưng không hiển thị, có thể do:
- User không có quyền
- Parent menu bị ẩn
- Groups không đúng

## Cách 4: Tạo Menu tạm thời ở vị trí dễ thấy

Nếu menu vẫn không hiển thị, có thể tạo menu ở vị trí khác:
- Dưới menu "Nhân viên" (nếu có)
- Dưới menu "Chấm công" (nếu có)
- Hoặc tạo menu root mới

## Cách 5: Test API trực tiếp

### Test Face Check-in (JSON API)
```bash
curl -X POST http://localhost:8069/face_attendance/check_in \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "image_data": "base64_encoded_image_here",
      "employee_id": 1
    }
  }'
```

## Kiểm tra Module đã được cài đặt

1. Vào **Apps** → Tìm "Custom HR Face Attendance"
2. Kiểm tra status: Phải là "Installed" (màu xanh)
3. Nếu chưa cài, click **Install**

## Test các tính năng

### 1. Test Face Registration
- Vào employee form
- Click button "Register Face"
- Upload ảnh và đăng ký

### 2. Test Face Check-in
- Dùng URL: `http://localhost:8069/face_attendance/checkin`
- Hoặc dùng API endpoint

### 3. Test Face Check-out
- Dùng URL: `http://localhost:8069/face_attendance/checkout`
- Hoặc dùng API endpoint

## Nếu vẫn không test được

1. Kiểm tra Python dependencies đã được cài:
   ```bash
   pip install opencv-python face-recognition numpy Pillow
   ```

2. Kiểm tra log Odoo xem có lỗi gì không

3. Kiểm tra model có tồn tại không:
   - Vào Developer Mode
   - Settings → Technical → Database Structure → Models
   - Tìm "face.registration"
