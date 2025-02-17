#!/bin/bash

# Exit on error
set -e

# Variables
DOMAIN="johnallens.com"
PROJECT_NAME="johnallens"
PROJECT_PATH="/var/www/$PROJECT_NAME"
PYTHON_VERSION="3.11"

echo "Starting deployment process for $DOMAIN..."

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv nginx supervisor certbot python3-certbot-nginx

# Create project directory
echo "Setting up project directory..."
sudo mkdir -p $PROJECT_PATH
sudo chown -R $USER:$USER $PROJECT_PATH

# Copy project files
echo "Copying project files..."
cp -r * $PROJECT_PATH/

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python$PYTHON_VERSION -m venv $PROJECT_PATH/venv
source $PROJECT_PATH/venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Set up Nginx
echo "Setting up Nginx..."
sudo cp nginx/johnallens.conf /etc/nginx/sites-available/$DOMAIN
sudo ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up SSL with Let's Encrypt
echo "Setting up SSL certificates..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# Set up Supervisor
echo "Setting up Supervisor..."
sudo cp supervisor/johnallens.conf /etc/supervisor/conf.d/
sudo mkdir -p /var/log/supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart $PROJECT_NAME

# Create log directories
echo "Setting up log directories..."
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn

# Set permissions
echo "Setting correct permissions..."
sudo chown -R www-data:www-data $PROJECT_PATH
sudo chmod -R 755 $PROJECT_PATH

echo "Deployment completed successfully!"
echo "Your site should now be accessible at https://$DOMAIN"
echo ""
echo "To check status:"
echo "1. Nginx: sudo systemctl status nginx"
echo "2. Supervisor: sudo supervisorctl status"
echo "3. Logs: tail -f /var/log/supervisor/johnallens.log"
