#!/bin/bash

# ============================================
# SIMURAZX BOT - Pterodactyl Startup Script
# ============================================

echo "========================================="
echo "  SIMURAZX PTERODACTYL BOT v1.0"
echo "  Starting bot..."
echo "========================================="

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update requirements
echo "[*] Installing dependencies..."
pip install -r requirements.txt --quiet

# Create data directory
mkdir -p data

# Run the bot
echo "[*] Starting bot..."
python3 bot.py

# Keep container alive
while true; do
    sleep 3600
done