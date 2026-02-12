#!/bin/bash
while true
do
    echo "🚀 Starting MakautAdminBot..."
    python3 run_production.py
    echo "⚠️ Bot crashed. Restarting in 5 seconds..."
    sleep 6
done