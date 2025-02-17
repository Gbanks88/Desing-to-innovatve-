#!/bin/bash
set -e

# Load environment variables
source .env

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting deployment for NJIC handle: ${YELLOW}${OVH_HANDLE}${NC}"

# Setup Python virtual environment
echo "Setting up Python environment..."
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup OVH resources
echo "Setting up OVH resources..."
python scripts/setup_njic_resources.py

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Deploy to OVH Object Storage
echo "Deploying frontend to OVH Storage..."
swift upload ${OVH_CONTAINER_NAME} frontend/dist/* \
    --segment-size 1073741824 \
    --segment-container frontend-segments

# Deploy backend
echo "Deploying backend..."
# Create systemd service file
cat > /etc/systemd/system/fashion-platform.service << EOL
[Unit]
Description=Fashion Platform Backend
After=network.target

[Service]
User=fashion
Group=fashion
WorkingDirectory=/opt/fashion-platform
Environment="PATH=/opt/fashion-platform/venv/bin"
ExecStart=/opt/fashion-platform/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and start service
systemctl daemon-reload
systemctl enable fashion-platform
systemctl restart fashion-platform

# Setup Nginx
echo "Configuring Nginx..."
cat > /etc/nginx/sites-available/fashion-platform << EOL
server {
    listen 80;
    server_name ${OVH_HANDLE}.fashionplatform.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl;
    server_name ${OVH_HANDLE}.fashionplatform.com;

    ssl_certificate /etc/letsencrypt/live/${OVH_HANDLE}.fashionplatform.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${OVH_HANDLE}.fashionplatform.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self' https: data: 'unsafe-inline' 'unsafe-eval';" always;

    # Frontend
    location / {
        root /var/www/fashion-platform;
        try_files \$uri \$uri/ /index.html;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # Rate limiting
        limit_req zone=api burst=20 nodelay;
        limit_req_status 429;
    }
}
EOL

# Enable site and restart Nginx
ln -sf /etc/nginx/sites-available/fashion-platform /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# Setup SSL certificate
echo "Setting up SSL certificate..."
certbot --nginx -d ${OVH_HANDLE}.fashionplatform.com --non-interactive --agree-tos -m ${OVH_EMAIL}

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "Your application is now available at: https://${OVH_HANDLE}.fashionplatform.com"
