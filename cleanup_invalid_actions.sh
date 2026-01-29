#!/bin/bash
# Script để cleanup các action window không hợp lệ trong Odoo

# Thay đổi tên database của bạn
DB_NAME="your_database_name"

echo "Đang cleanup các action window không hợp lệ..."

# Chạy Python script trong Odoo shell
python3 odoo-bin shell -d "$DB_NAME" <<EOF
# Lấy danh sách tất cả các model hợp lệ
valid_models = set(env.registry.keys())

# Tìm các action window có res_model không tồn tại
invalid_actions = env['ir.actions.act_window'].search([])
fixed_count = 0

for action in invalid_actions:
    if action.res_model and action.res_model not in valid_models:
        print(f"Tìm thấy action không hợp lệ: ID={action.id}, name={action.name}, res_model={action.res_model}")
        # Vô hiệu hóa action bằng cách xóa res_model
        action.write({'res_model': False})
        print(f"  -> Đã vô hiệu hóa action ID {action.id}")
        fixed_count += 1

print(f"\nTổng cộng đã fix {fixed_count} action(s)")
env.cr.commit()
EOF

echo "Hoàn thành!"
