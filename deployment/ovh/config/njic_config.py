from typing import Dict
import os

class NJICConfig:
    """NJIC Configuration for OVH Services"""
    
    HANDLE = "bg1274099-ovh"
    
    @staticmethod
    def get_ovh_config() -> Dict[str, str]:
        """Get OVH configuration with NJIC handle"""
        return {
            'NJIC_HANDLE': NJICConfig.HANDLE,
            'OVH_ENDPOINT': 'ovh-us',
            'OVH_REGION': 'BHS',  # Beauharnois (North America)
            'OVH_TENANT_NAME': f'njic_{NJICConfig.HANDLE}',
            'OVH_PROJECT_NAME': f'fashion_platform_{NJICConfig.HANDLE}',
            
            # Storage configuration
            'OVH_STORAGE_NAME': f'fashion_storage_{NJICConfig.HANDLE}',
            'OVH_CONTAINER_NAME': 'fashion-assets',
            
            # Database configuration
            'OVH_DB_NAME': f'fashion_db_{NJICConfig.HANDLE}',
            
            # Email configuration
            'OVH_EMAIL_DOMAIN': 'fashionplatform.com',
            'OVH_EMAIL_PREFIX': f'admin.{NJICConfig.HANDLE}',
            
            # Backup configuration
            'OVH_BACKUP_CONTAINER': f'backups_{NJICConfig.HANDLE}'
        }

    @staticmethod
    def get_environment_vars() -> Dict[str, str]:
        """Generate environment variables for deployment"""
        config = NJICConfig.get_ovh_config()
        return {
            # OVH API Credentials
            'OVH_HANDLE': config['NJIC_HANDLE'],
            'OVH_ENDPOINT': config['OVH_ENDPOINT'],
            'OVH_REGION': config['OVH_REGION'],
            
            # Project Configuration
            'OVH_PROJECT_NAME': config['OVH_PROJECT_NAME'],
            'OVH_TENANT_NAME': config['OVH_TENANT_NAME'],
            
            # Storage Configuration
            'OVH_STORAGE_NAME': config['OVH_STORAGE_NAME'],
            'OVH_CONTAINER_NAME': config['OVH_CONTAINER_NAME'],
            'OVH_STORAGE_URL': f"https://storage.{config['OVH_REGION']}.cloud.ovh.net/v1/AUTH_{config['NJIC_HANDLE']}",
            
            # Database Configuration
            'MONGODB_URL': f"mongodb://[username]:[password]@mongodb.{config['OVH_REGION']}.cloud.ovh.net:27017/{config['OVH_DB_NAME']}",
            'MONGODB_DB_NAME': config['OVH_DB_NAME'],
            
            # Email Configuration
            'OVH_EMAIL': f"{config['OVH_EMAIL_PREFIX']}@{config['OVH_EMAIL_DOMAIN']}",
            
            # Backup Configuration
            'OVH_BACKUP_CONTAINER': config['OVH_BACKUP_CONTAINER'],
            'BACKUP_RETENTION_DAYS': '30'
        }

    @staticmethod
    def generate_env_file():
        """Generate .env file content"""
        env_vars = NJICConfig.get_environment_vars()
        return '\n'.join([f'{k}={v}' for k, v in env_vars.items()])
