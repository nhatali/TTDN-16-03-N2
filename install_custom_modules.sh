#!/bin/bash
# Script to install/upgrade HR, Attendance, and Document Management modules

echo "========================================"
echo "Installing/Upgrading Odoo Modules"
echo "========================================"

# Change to Odoo directory
cd /home/minhtien/Business-Internship

# Update module list and upgrade modules
echo "Updating module list..."
./odoo-bin -c odoo.conf -d odoo_db --stop-after-init --update=nhan_su,cham_cong,quan_ly_van_ban

echo "========================================"
echo "Module installation completed!"
echo "Please restart Odoo to see the changes."
echo "========================================"
