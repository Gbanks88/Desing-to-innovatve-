# OVHcloud Deployment Guide

## Step 1: Account Setup
1. Visit [OVHcloud website](https://www.ovhcloud.com/)
2. Create an account
3. Verify your identity (required for European hosting)
4. Add a payment method

## Step 2: Server Selection
1. Go to "Bare Metal and Shared Hosting"
2. Choose "VPS" or "Dedicated Servers"
3. Recommended configuration:
   ```
   VPS Elite
   - 8 vCores
   - 16GB RAM
   - 256GB SSD NVMe
   - Unlimited traffic
   ```
4. Select datacenter location:
   - Gravelines, France (EU)
   - Beauharnois, Canada (NA)

## Step 3: Initial Server Setup
```bash
# 1. SSH into your server
ssh root@your-server-ip

# 2. Update system
apt update && apt upgrade -y

# 3. Install required packages
apt install -y \
    docker.io \
    docker-compose \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw

# 4. Start and enable Docker
systemctl start docker
systemctl enable docker

# 5. Configure firewall
ufw allow ssh
ufw allow http
ufw allow https
ufw enable
```

## Step 4: Domain Configuration
1. In OVHcloud control panel:
   - Add your domain
   - Point nameservers to OVH
   - Create DNS records:
   ```
   A     @     your-server-ip
   A     www   your-server-ip
   A     api   your-server-ip
   ```

2. SSL Certificate setup:
   ```bash
   certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
   ```

## Step 5: Project Deployment
1. Clone your repository:
   ```bash
   git clone your-repository
   cd your-repository
   ```

2. Create environment file:
   ```bash
   cd deployment/ovh
   cp .env.example .env
   nano .env
   ```

3. Configure environment variables:
   ```env
   MONGO_ROOT_USER=your_username
   MONGO_ROOT_PASSWORD=your_secure_password
   MONGODB_URL=mongodb://your_username:your_secure_password@mongodb:27017/fashion_platform
   JWT_SECRET=your_jwt_secret
   ```

4. Start the services:
   ```bash
   docker-compose -f docker-compose.ovh.yml up -d
   ```

## Step 6: Monitoring Setup
1. Access OVHcloud metrics:
   - Log into OVHcloud control panel
   - Go to "Metrics" section
   - Enable monitoring

2. Set up alerts:
   ```bash
   # CPU Usage alert
   ovh-alert set cpu 80

   # Memory Usage alert
   ovh-alert set memory 85

   # Disk Usage alert
   ovh-alert set disk 85
   ```

## Step 7: Backup Configuration
1. Verify backup script permissions:
   ```bash
   chmod +x scripts/backup.sh
   ```

2. Test backup system:
   ```bash
   docker-compose -f docker-compose.ovh.yml exec backup /scripts/backup.sh
   ```

3. Set up daily backups:
   ```bash
   crontab -e
   # Add line:
   0 2 * * * docker-compose -f /path/to/docker-compose.ovh.yml exec backup /scripts/backup.sh
   ```

## Step 8: Security Hardening
1. Enable OVH firewall:
   - Go to OVH control panel
   - Navigate to server security
   - Enable anti-DDoS protection

2. Configure fail2ban:
   ```bash
   apt install fail2ban
   cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
   systemctl enable fail2ban
   systemctl start fail2ban
   ```

## Step 9: Performance Optimization
1. Configure Nginx caching:
   ```bash
   # Edit nginx configuration
   nano /etc/nginx/nginx.conf
   ```

2. Enable Gzip compression:
   ```nginx
   gzip on;
   gzip_types text/plain application/json;
   gzip_min_length 1000;
   ```

## Step 10: Maintenance
1. Regular updates:
   ```bash
   # Update system packages
   apt update && apt upgrade -y

   # Update Docker images
   docker-compose -f docker-compose.ovh.yml pull
   docker-compose -f docker-compose.ovh.yml up -d
   ```

2. Monitor logs:
   ```bash
   # View application logs
   docker-compose -f docker-compose.ovh.yml logs -f

   # View specific service logs
   docker-compose -f docker-compose.ovh.yml logs -f backend
   ```

## Support and Troubleshooting
- OVH Support: https://help.ovhcloud.com
- Emergency contact: +1 855-684-5463 (NA) / +353 1 293 7844 (EU)
- Technical support available 24/7

## Cost Management
1. Monitor usage in OVH control panel
2. Set up billing alerts
3. Review monthly invoices
4. Scale resources as needed

## Scaling Guidelines
1. Vertical Scaling:
   - Upgrade VPS plan through OVH control panel
   - No downtime required

2. Horizontal Scaling:
   - Add additional servers
   - Configure load balancing
   - Distribute database load

Remember to:
- Keep regular backups
- Monitor system performance
- Update security patches
- Review logs regularly
- Test disaster recovery plan
