#!/bin/bash
# Script to fix port 8069 issue

echo "=== Fixing Odoo Port 8069 Issue ==="
echo ""

# Find process using port 8069
echo "1. Finding process on port 8069..."
PID=$(lsof -ti:8069 2>/dev/null)

if [ ! -z "$PID" ]; then
    echo "   Found process with PID: $PID"
    echo "2. Killing process $PID..."
    kill -9 $PID 2>/dev/null
    sleep 2
    echo "   Process killed!"
else
    echo "   No process found on port 8069"
fi

# Also check for any odoo-bin processes
echo ""
echo "3. Checking for other Odoo processes..."
ODOO_PIDS=$(ps aux | grep odoo-bin | grep -v grep | awk '{print $2}')

if [ ! -z "$ODOO_PIDS" ]; then
    echo "   Found Odoo processes: $ODOO_PIDS"
    echo "   Killing them..."
    echo "$ODOO_PIDS" | xargs kill -9 2>/dev/null
    sleep 2
    echo "   Done!"
else
    echo "   No other Odoo processes found"
fi

echo ""
echo "4. Verifying port 8069 is free..."
if lsof -ti:8069 > /dev/null 2>&1; then
    echo "   WARNING: Port 8069 is still in use!"
    echo "   You may need to manually kill the process or change the port in odoo.conf"
else
    echo "   ✓ Port 8069 is now free!"
    echo ""
    echo "You can now start Odoo with: ./odoo-bin -c odoo.conf"
fi
