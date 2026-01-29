# Hướng Dẫn Tìm Module Khi Không Có Nút Update Apps List

## Cách 1: Bật Developer Mode (Khuyến nghị)

1. Vào **Settings** (Thiết lập) ở menu trên
2. Kéo xuống cuối trang, tìm phần **Activate Developer Mode**
3. Click để bật Developer Mode
4. Sau khi bật, quay lại **Apps** - bạn sẽ thấy nhiều tùy chọn hơn
5. Tìm kiếm module: `nhan_su`, `cham_cong`, `tien_luong`

## Cách 2: Tìm Module Trực Tiếp

1. Vào **Apps**
2. Ở ô tìm kiếm, gõ: `nhan su` hoặc `Nhân Sự`
3. Hoặc gõ: `cham cong` hoặc `Chấm Công`
4. Hoặc gõ: `tien luong` hoặc `Tiền Lương`

Nếu module đã có trong hệ thống, nó sẽ hiển thị ngay cả khi chưa cài đặt.

## Cách 3: Update Qua Command Line (Chắc chắn nhất)

Chạy lệnh này trong terminal:

```bash
# Thay 'odoo' bằng tên database của bạn
python3 odoo-bin -c odoo.conf -d odoo --stop-after-init
```

Sau đó restart server:
```bash
python3 odoo-bin -c odoo.conf
```

## Cách 4: Kiểm Tra Module Có Tồn Tại Không

Nếu module không hiển thị sau khi update, có thể do:

1. **Module chưa được load**: Kiểm tra log Odoo khi khởi động
2. **Lỗi trong manifest**: Module bị đánh dấu "not installable"
3. **Đường dẫn addons sai**: Kiểm tra file `odoo.conf`

## Cách 5: Tìm Module Qua Settings (Nếu có quyền Admin)

1. Vào **Settings** → **Apps** → **Apps**
2. Tìm kiếm module ở đây
3. Nếu thấy, có thể cài đặt trực tiếp

## Kiểm Tra Module Có Tồn Tại

Chạy lệnh này để kiểm tra module có được Odoo nhận diện không:

```bash
python3 odoo-bin -c odoo.conf -d odoo --stop-after-init 2>&1 | grep -i "nhan_su\|cham_cong\|tien_luong"
```

Nếu thấy tên module trong output, nghĩa là Odoo đã nhận diện được.

## Nếu Vẫn Không Thấy

1. **Kiểm tra log khi khởi động Odoo** - xem có lỗi gì về module không
2. **Kiểm tra file manifest** - đảm bảo `installable: True`
3. **Kiểm tra đường dẫn addons** trong `odoo.conf`:
   ```ini
   addons_path = addons
   ```
   Phải đảm bảo đường dẫn này trỏ đến thư mục chứa `btl/`
