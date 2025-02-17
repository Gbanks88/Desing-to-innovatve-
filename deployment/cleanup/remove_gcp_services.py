from google.cloud import storage
from google.cloud import compute_v1
from google.cloud import container_v1
from google.cloud import monitoring_v3
import os

class GCPCleanup:
    def __init__(self):
        self.project_id = os.getenv('GCP_PROJECT_ID')
        
    def delete_storage_buckets(self):
        """Delete all storage buckets"""
        print("Deleting storage buckets...")
        storage_client = storage.Client()
        
        for bucket in storage_client.list_buckets():
            print(f"Deleting bucket: {bucket.name}")
            bucket.delete(force=True)
            
    def delete_compute_instances(self):
        """Delete all compute instances"""
        print("Deleting compute instances...")
        instance_client = compute_v1.InstancesClient()
        
        for zone in self.list_zones():
            request = compute_v1.ListInstancesRequest(
                project=self.project_id,
                zone=zone
            )
            instances = instance_client.list(request=request)
            
            for instance in instances:
                print(f"Deleting instance: {instance.name}")
                operation = instance_client.delete(
                    project=self.project_id,
                    zone=zone,
                    instance=instance.name
                )
                operation.result()  # Wait for deletion
                
    def delete_gke_clusters(self):
        """Delete all GKE clusters"""
        print("Deleting GKE clusters...")
        cluster_client = container_v1.ClusterManagerClient()
        
        parent = f"projects/{self.project_id}/locations/-"
        request = container_v1.ListClustersRequest(parent=parent)
        
        try:
            clusters = cluster_client.list_clusters(request=request)
            for cluster in clusters.clusters:
                print(f"Deleting cluster: {cluster.name}")
                name = f"projects/{self.project_id}/locations/{cluster.location}/clusters/{cluster.name}"
                request = container_v1.DeleteClusterRequest(name=name)
                operation = cluster_client.delete_cluster(request=request)
                operation.result()  # Wait for deletion
        except Exception as e:
            print(f"Error deleting clusters: {str(e)}")
                
    def delete_monitoring(self):
        """Delete all monitoring resources"""
        print("Deleting monitoring resources...")
        client = monitoring_v3.AlertPolicyServiceClient()
        
        try:
            parent = f"projects/{self.project_id}"
            policies = client.list_alert_policies(request={"name": parent})
            
            for policy in policies:
                print(f"Deleting alert policy: {policy.name}")
                client.delete_alert_policy(request={"name": policy.name})
        except Exception as e:
            print(f"Error deleting monitoring resources: {str(e)}")
    
    def list_zones(self):
        """List all available zones"""
        zones_client = compute_v1.ZonesClient()
        request = compute_v1.ListZonesRequest(
            project=self.project_id
        )
        return [zone.name for zone in zones_client.list(request=request)]
    
    def cleanup_all(self):
        """Run all cleanup operations"""
        print(f"Starting cleanup for project: {self.project_id}")
        
        try:
            self.delete_storage_buckets()
            self.delete_compute_instances()
            self.delete_gke_clusters()
            self.delete_monitoring()
            
            print("\nCleanup completed successfully!")
            print("Please verify in the GCP Console that all resources have been removed")
            print("Note: Some resources might require manual deletion due to dependencies")
            
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
            raise

if __name__ == "__main__":
    cleanup = GCPCleanup()
    cleanup.cleanup_all()
