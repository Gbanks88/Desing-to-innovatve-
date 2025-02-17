import os
import sys
import ovh
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config.njic_config import NJICConfig

class OVHResourceManager:
    def __init__(self):
        self.config = NJICConfig.get_ovh_config()
        self.client = ovh.Client(
            endpoint=os.getenv('OVH_ENDPOINT', 'ovh-us'),
            application_key=os.getenv('OVH_APPLICATION_KEY'),
            application_secret=os.getenv('OVH_APPLICATION_SECRET'),
            consumer_key=os.getenv('OVH_CONSUMER_KEY')
        )

    def setup_project(self):
        """Create or get project"""
        try:
            project = self.client.post('/cloud/project', 
                description=f"Fashion Platform - {self.config['NJIC_HANDLE']}")
            print(f"Created project: {project['project_id']}")
            return project['project_id']
        except ovh.exceptions.ResourceConflictError:
            projects = self.client.get('/cloud/project')
            for project_id in projects:
                details = self.client.get(f'/cloud/project/{project_id}')
                if details['description'] == f"Fashion Platform - {self.config['NJIC_HANDLE']}":
                    print(f"Found existing project: {project_id}")
                    return project_id
            raise Exception("Could not find or create project")

    def setup_object_storage(self, project_id):
        """Set up object storage containers"""
        containers = [
            self.config['OVH_CONTAINER_NAME'],
            self.config['OVH_BACKUP_CONTAINER']
        ]
        
        for container in containers:
            try:
                self.client.post(f'/cloud/project/{project_id}/storage', 
                    container=container,
                    region=self.config['OVH_REGION'])
                print(f"Created container: {container}")
            except ovh.exceptions.ResourceConflictError:
                print(f"Container already exists: {container}")

    def setup_database(self, project_id):
        """Set up MongoDB database"""
        try:
            db = self.client.post(f'/cloud/project/{project_id}/database/mongodb',
                name=self.config['OVH_DB_NAME'],
                region=self.config['OVH_REGION'],
                version='6.0',
                plan='essential')
            print(f"Created MongoDB database: {db['id']}")
            return db['id']
        except ovh.exceptions.ResourceConflictError:
            print("Database already exists")

    def setup_email(self):
        """Set up Email Pro service"""
        try:
            email = self.client.post('/email/pro',
                domain=self.config['OVH_EMAIL_DOMAIN'])
            print(f"Created Email Pro service for domain: {self.config['OVH_EMAIL_DOMAIN']}")
            
            # Create admin email account
            self.client.post(f'/email/pro/{self.config["OVH_EMAIL_DOMAIN"]}/account',
                accountName=f"admin.{self.config['NJIC_HANDLE']}")
            print(f"Created admin email account: {self.config['OVH_EMAIL']}")
            
        except ovh.exceptions.ResourceConflictError:
            print("Email service already exists")

    def setup_security(self, project_id):
        """Set up security configurations"""
        # Configure network security groups
        try:
            sg = self.client.post(f'/cloud/project/{project_id}/network/security/group',
                name=f"fashion-sg-{self.config['NJIC_HANDLE']}",
                description="Fashion Platform Security Group")
            
            # Allow HTTP/HTTPS
            self.client.post(f'/cloud/project/{project_id}/network/security/group/{sg["id"]}/rule',
                direction='inbound', protocol='TCP', portFrom=80, portTo=80)
            self.client.post(f'/cloud/project/{project_id}/network/security/group/{sg["id"]}/rule',
                direction='inbound', protocol='TCP', portFrom=443, portTo=443)
            
            # Allow MongoDB
            self.client.post(f'/cloud/project/{project_id}/network/security/group/{sg["id"]}/rule',
                direction='inbound', protocol='TCP', portFrom=27017, portTo=27017)
            
            print("Created security group with rules")
        except ovh.exceptions.ResourceConflictError:
            print("Security group already exists")

    def setup_all(self):
        """Set up all OVH resources"""
        try:
            print(f"Starting setup for NJIC handle: {self.config['NJIC_HANDLE']}")
            
            # Create project
            project_id = self.setup_project()
            
            # Setup resources
            self.setup_object_storage(project_id)
            self.setup_database(project_id)
            self.setup_email()
            self.setup_security(project_id)
            
            print("\nSetup completed successfully!")
            print("Please check the OVH control panel for resource details and credentials")
            
        except Exception as e:
            print(f"Error during setup: {str(e)}")
            raise

if __name__ == "__main__":
    manager = OVHResourceManager()
    manager.setup_all()
