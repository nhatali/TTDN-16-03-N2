# Hướng Dẫn Fix Cuối Cùng - Module "Not Installable"

## 🔍 Nguyên nhân

Module nằm trong `addons/btl/nhan_su/` nhưng **Odoo chỉ scan các module trực tiếp trong `addons/`**.

Odoo không tìm thấy module → đánh dấu "not installable".

## ✅ Giải pháp: Di chuyển module ra ngoài

### Cách 1: Dùng script (Khuyến nghị)

```bash
chmod +x move_modules.sh
./move_modules.sh
```

### Cách 2: Di chuyển thủ công

```bash
cd ~/Business-Internship/addons

# Di chuyển các module
mv btl/nhan_su .
mv btl/cham_cong .
mv btl/tien_luong .
```

## 📋 Sau khi di chuyển

### Bước 1: Update module list

```bash
python3 odoo-bin -c odoo.conf -d odoo --stop-after-init
```

### Bước 2: Restart server

```bash
python3 odoo-bin -c odoo.conf
```

### Bước 3: Vào Odoo và tìm module

1. Vào **Apps**
2. Tìm kiếm: `nhan su`, `cham cong`, `tien luong`
3. Module sẽ hiển thị và có thể cài đặt!

## ⚠️ Lưu ý

Sau khi di chuyển, các file static trong `btl/static/` sẽ không được load. Nhưng module vẫn hoạt động bình thường (chỉ thiếu widget camera).

Nếu cần widget camera, có thể:
- Di chuyển static files vào từng module
- Hoặc tạo module `btl` riêng để chứa shared assets

## 🎯 Kết quả mong đợi

Sau khi di chuyển và update, log sẽ không còn:
- ❌ `module nhan_su: not installable, skipped`
- ❌ `module cham_cong: not installable, skipped`

Thay vào đó sẽ thấy:
- ✅ Module được load thành công
- ✅ Module hiển thị trong Apps
- ✅ Có thể cài đặt được
