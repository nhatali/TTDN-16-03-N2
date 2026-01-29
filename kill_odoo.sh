#!/bin/bash
# Script to kill Odoo processes on port 8069

echo "Checking for processes on port 8069..."
PID=$(lsof -ti:8069 2>/dev/null || fuser 8069/tcp 2>/dev/null | awk '{print $1}')

if [ -z "$PID" ]; then
    echo "No process found on port 8069"
    echo "Checking for odoo-bin processes..."
    PID=$(ps aux | grep odoo-bin | grep -v grep | awk '{print $2}' | head -1)
fi

if [ ! -z "$PID" ]; then
    echo "Found process with PID: $PID"
    echo "Killing process..."
    kill -9 $PID
    echo "Process killed successfully"
    sleep 2
else
    echo "No Odoo process found to kill"
fi
