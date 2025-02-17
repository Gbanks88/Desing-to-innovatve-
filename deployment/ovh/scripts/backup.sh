#!/bin/bash

# Configuration
BACKUP_DIR="/backup"
MONGODB_HOST="mongodb"
MONGODB_PORT="27017"
MONGODB_USER="${MONGO_ROOT_USER}"
MONGODB_PASSWORD="${MONGO_ROOT_PASSWORD}"
DATABASE="fashion_platform"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_PATH="${BACKUP_DIR}/${DATABASE}_${DATE}"

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Perform backup
mongodump \
  --host ${MONGODB_HOST} \
  --port ${MONGODB_PORT} \
  --username ${MONGODB_USER} \
  --password ${MONGODB_PASSWORD} \
  --db ${DATABASE} \
  --out ${BACKUP_PATH}

# Compress backup
tar -czf ${BACKUP_PATH}.tar.gz ${BACKUP_PATH}
rm -rf ${BACKUP_PATH}

# Delete backups older than 30 days
find ${BACKUP_DIR} -type f -name "*.tar.gz" -mtime +30 -delete

# Log backup completion
echo "Backup completed: ${BACKUP_PATH}.tar.gz"
