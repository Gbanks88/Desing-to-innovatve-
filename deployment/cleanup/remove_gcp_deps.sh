#!/bin/bash

# Remove GCP-related packages from requirements.txt
sed -i '/google-cloud/d' backend/requirements.txt
sed -i '/google-auth/d' backend/requirements.txt
sed -i '/google-api/d' backend/requirements.txt

# Remove GCP configuration files
rm -f backend/config/gcp_config.py
rm -f backend/config/gcp_credentials.json

# Remove GCP environment variables from .env files
sed -i '/GOOGLE_/d' backend/.env
sed -i '/GCP_/d' backend/.env

# Remove GCP-related directories
rm -rf deployment/gcp/

echo "GCP dependencies removed successfully!"
