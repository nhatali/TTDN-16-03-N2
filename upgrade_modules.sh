#!/bin/bash

# Kill existing Odoo processes
pkill -f 'python.*odoo-bin' 2>/dev/null || true

echo "Starting Odoo module upgrade..."

# Upgrade modules
python3 odoo-bin -c odoo.conf -u nhan_su,cham_cong,tinh_luong -d business_db --stop-after-init

echo "Module upgrade completed!"
