#!/usr/bin/env bash
set -euo pipefail

# Verify root privileges
if [[ $EUID -ne 0 ]]; then
   echo "ERROR: This script must be run as root (or via sudo)." >&2
   exit 1
fi

# Check for required environment variable
if [[ -z "${API_KEY:-}" ]]; then
    echo "ERROR: API_KEY environment variable is not set." >&2
    echo "Usage: sudo API_KEY=your_secret ./install.sh" >&2
    exit 1
fi

# Set sensible defaults
PORT=${PORT:-5000}
VERSION=${VERSION:-"1.0.0"}

echo "--- Building the Docker image ---"
docker build -t status-dashboard .

echo "--- Cleaning up old container (Idempotency) ---"
docker rm -f status-dashboard 2>/dev/null || true

echo "--- Starting the container ---"
docker run -d \
  --name status-dashboard \
  --restart unless-stopped \
  -p 127.0.0.1:5000:5000 \
  -e PORT="${PORT}" \
  -e VERSION="${VERSION}" \
  -e API_KEY="${API_KEY}" \
  status-dashboard

echo "--- Configuring Nginx ---"
cp nginx/status-dashboard /etc/nginx/sites-available/
ln -sf /etc/nginx/sites-available/status-dashboard /etc/nginx/sites-enabled/

# Disable default site
rm -f /etc/nginx/sites-enabled/default

echo "--- Validating Nginx configuration ---"
nginx -t

echo "--- Enabling and Reloading Nginx ---"
systemctl enable nginx
systemctl reload nginx

# Get the vm ip to display to the user
VM_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "=========================================================="
echo "SUCCESS! Service is up and running."
echo "You can reach the Status Dashboard at: http://${VM_IP}/"
echo "=========================================================="
