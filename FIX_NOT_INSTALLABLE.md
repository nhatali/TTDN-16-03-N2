# Fix Module "Not Installable"

## Vấn đề
Module bị đánh dấu "not installable, skipped" mặc dù:
- ✅ Python syntax không có lỗi
- ✅ Manifest có `installable: True`

## Nguyên nhân có thể

### 1. Odoo không tìm thấy module trong đúng đường dẫn
Module nằm trong `addons/btl/nhan_su/` nhưng Odoo có thể không scan thư mục `btl/`.

### 2. Lỗi khi import trong __init__.py
Khi Odoo import `__init__.py`, nếu có lỗi → đánh dấu "not installable".

## Giải pháp

### Cách 1: Di chuyển module ra ngoài thư mục btl

Module phải nằm trực tiếp trong `addons/`, không nên nằm trong subfolder:

```bash
# Di chuyển module
mv addons/btl/nhan_su addons/nhan_su
mv addons/btl/cham_cong addons/cham_cong
mv addons/btl/tien_luong addons/tien_luong
```

Sau đó update lại:
```bash
python3 odoo-bin -c odoo.conf -d odoo --stop-after-init
```

### Cách 2: Kiểm tra xem Odoo có scan thư mục btl không

Odoo chỉ scan các thư mục trực tiếp trong `addons_path`. Nếu module nằm trong `addons/btl/`, Odoo sẽ không tìm thấy trừ khi:
- Có file `__init__.py` và `__manifest__.py` trong `addons/btl/` (để biến nó thành module)
- Hoặc di chuyển module ra ngoài

### Cách 3: Tạo module btl wrapper

Tạo `addons/btl/__manifest__.py` để biến `btl` thành module, nhưng cách này phức tạp.

## Khuyến nghị

**Cách đơn giản nhất**: Di chuyển module ra ngoài thư mục `btl/`
