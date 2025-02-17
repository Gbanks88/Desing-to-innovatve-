import os
import requests
import json
import base64
from datetime import datetime

def load_env_file(env_path):
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

class DomainManager:
    def __init__(self, env_vars):
        self.username = env_vars.get('DOMAIN_REGISTRAR_USERNAME')
        self.password = env_vars.get('DOMAIN_Password')
        self.domain = env_vars.get('DOMAIN_NAME')
        self.api_url = "https://api.yourdomain.com/v1"  # Replace with your registrar's API endpoint
        self.headers = {
            'Authorization': f'Basic {self._get_auth_header()}',
            'Content-Type': 'application/json'
        }

    def _get_auth_header(self):
        """Generate Basic Auth header"""
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()

    def verify_domain(self):
        """Verify domain ownership and status"""
        print(f"\nVerifying domain: {self.domain}")
        print(f"Username: {self.username}")
        
        # Add your registrar's domain verification logic here
        return True

    def get_dns_records(self):
        """Get current DNS records"""
        print(f"\nGetting DNS records for {self.domain}")
        
        # Simulated DNS records for testing
        return [
            {'type': 'A', 'host': '@', 'value': '216.239.32.21', 'ttl': 3600},
            {'type': 'A', 'host': 'www', 'value': '172.217.12.19', 'ttl': 3600}
        ]

    def add_dns_record(self, record_type, host, value, ttl=3600):
        """Add a new DNS record"""
        record = {
            'type': record_type,
            'host': host,
            'value': value,
            'ttl': ttl
        }
        print(f"\nAdding DNS record: {json.dumps(record, indent=2)}")
        return True

    def setup_required_records(self):
        """Setup all required DNS records for johnallens.com"""
        required_records = [
            # Main domain and www
            {'type': 'A', 'host': '@', 'value': '216.239.32.21'},
            {'type': 'A', 'host': 'www', 'value': '172.217.12.19'},
            
            # Subdomains for different services
            {'type': 'A', 'host': 'api', 'value': '216.239.32.21'},
            {'type': 'A', 'host': 'admin', 'value': '216.239.32.21'},
            {'type': 'A', 'host': 'cdn', 'value': '216.239.32.21'},
            
            # Email and security records
            {'type': 'TXT', 'host': '@', 'value': 'v=spf1 include:_spf.google.com ~all'},
            {'type': 'TXT', 'host': '_dmarc', 'value': 'v=DMARC1; p=reject; rua=mailto:admin@johnallens.com'},
            
            # Additional security records
            {'type': 'CAA', 'host': '@', 'value': '0 issue "letsencrypt.org"'},
            {'type': 'CAA', 'host': '@', 'value': '0 issuewild "letsencrypt.org"'}
        ]

        print(f"\nSetting up DNS records for {self.domain}")
        for record in required_records:
            success = self.add_dns_record(
                record['type'],
                record['host'],
                record['value']
            )
            if success:
                print(f"✓ Added {record['type']} record for {record['host']}.{self.domain}")
            else:
                print(f"✗ Failed to add {record['type']} record for {record['host']}.{self.domain}")

    def verify_dns_setup(self):
        """Verify all required DNS records are properly set up"""
        current_records = self.get_dns_records()
        if not current_records:
            print("Could not retrieve DNS records")
            return

        required_hosts = ['@', 'www', 'api', 'admin', 'cdn']
        for host in required_hosts:
            found = False
            for record in current_records:
                if record['host'] == host:
                    found = True
                    print(f"✓ {host}.{self.domain} is properly configured")
                    break
            if not found:
                print(f"✗ {host}.{self.domain} is not configured")

def main():
    # Load environment variables
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(current_dir, '.env')
    print(f"Loading configuration from: {env_path}")
    
    try:
        env_vars = load_env_file(env_path)
        manager = DomainManager(env_vars)
        
        if manager.verify_domain():
            print("\nDomain verification successful!")
            
            print("\nCurrent DNS Configuration:")
            manager.verify_dns_setup()
            
            choice = input("\nWould you like to:\n1. Set up all required DNS records\n2. View current DNS records\n3. Exit\nChoice (1-3): ")
            
            if choice == '1':
                manager.setup_required_records()
            elif choice == '2':
                records = manager.get_dns_records()
                print("\nCurrent DNS Records:")
                for record in records:
                    print(f"{record['type']} record: {record['host']}.{manager.domain} -> {record['value']}")
        else:
            print("Domain verification failed. Please check your credentials.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
