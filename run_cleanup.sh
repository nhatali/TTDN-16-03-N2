#!/bin/bash
# Cleanup script to remove old face recognition module

export PGPASSWORD=odoo
psql -h localhost -p 5431 -U odoo -d odoo -f cleanup_old_face_module.sql
echo "Cleanup completed!"
