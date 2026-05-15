#!/bin/bash
# SCAMEATER - VPS Provisioning Script
# Run this script after creating a fresh Ubuntu 22.04 VPS
# Usage: bash <(curl -sL https://your-repo/raw/main/infra/provision-vps.sh)

set -e

echo "=== SCAMEATER VPS Provisioning ==="
echo "This script will set up a VPS for SCAMEATER"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo $0"
    exit 1
fi

echo "[1/8] Updating system..."
apt update && apt upgrade -y

echo "[2/8] Installing base packages..."
apt install -y \
    curl wget git vim \
    build-essential \
    python3 python3-venv python3-pip \
    ffmpeg libsndfile1 portaudio19-dev \
    ufw nginx certbot python3-certbot-nginx

echo "[3/8] Installing Docker..."
curl -fsSL https://get.docker.com | sh
systemctl enable docker
systemctl start docker

echo "[4/8] Installing Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "[5/8] Configuring firewall..."
ufw allow 22/tcp
ufw allow 5060/udp
ufw allow 5060/tcp
ufw allow 10000:20000/udp
ufw allow 8501/tcp
ufw allow 8000/tcp
ufw allow 9001/tcp
echo "y" | ufw enable

echo "[6/8] Creating scameater user..."
useradd -m -s /bin/bash -G docker scameater 2>/dev/null || true
mkdir -p /opt/scameater
chown -R scameater:scameater /opt/scameater

echo "[7/8] Cloning repository..."
# REPLACE with your actual repository URL
# su - scameater -c "git clone https://github.com/youruser/scameater.git /opt/scameater"
echo "NOTE: Clone the repository manually as scameater user"

echo "[8/8] Setting up SSL with Let's Encrypt..."
# nginx -t && systemctl reload nginx
# certbot --nginx -d yourdomain.com --noninteractive --agree-tos -m your@email.com

echo ""
echo "=== Provisioning Complete ==="
echo ""
echo "Next steps:"
echo "1. cd /opt/scameater"
echo "2. cp .env.example .env"
echo "3. Edit .env with your API keys"
echo "4. docker compose up -d"
echo "5. docker exec scameater-engine python scripts/init_db.py"
echo ""
echo "Access:"
echo "  Dashboard: http://your-vps-ip:8501"
echo "  API: http://your-vps-ip:8000"
echo ""