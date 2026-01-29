# Fix Lỗi RPC_ERROR - KeyError: 'nhan_vien'

## Vấn đề

Lỗi xảy ra vì có action window cũ trong database đang tham chiếu đến model `nhan_vien` (tên cũ) nhưng model hiện tại là `nhan.su`.

## Giải pháp

### Bước 1: Chạy script cleanup

```bash
python3 cleanup_old_actions.py
```

Script này sẽ:
- Tìm tất cả action window có `res_model` không tồn tại
- Vô hiệu hóa chúng bằng cách xóa `res_model`
- Commit vào database

### Bước 2: Restart Odoo Server

```bash
# Dừng server (Ctrl+C)
# Khởi động lại
python3 odoo-bin -c odoo.conf
```

### Bước 3: Kiểm tra lại

Sau khi restart, lỗi sẽ không còn xuất hiện nữa.

## Lưu ý

- Script sẽ không xóa action, chỉ vô hiệu hóa bằng cách xóa `res_model`
- Nếu muốn xóa hoàn toàn, có thể sửa script để dùng `action.unlink()` thay vì `action.write({'res_model': False})`
- Code đã được sửa trong `ir_actions.py` để tự động xử lý các trường hợp này trong tương lai

## Nếu vẫn còn lỗi

Nếu sau khi cleanup vẫn còn lỗi, có thể do:
1. Có record khác (không phải action) đang tham chiếu model cũ
2. Cần kiểm tra log Odoo để xem model nào đang bị lỗi

Gửi cho tôi log Odoo để tôi có thể fix tiếp.
