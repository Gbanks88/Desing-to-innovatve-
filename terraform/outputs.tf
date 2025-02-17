output "droplet_ip" {
  value       = digitalocean_droplet.web.ipv4_address
  description = "The public IP address of the web server"
}

output "spaces_endpoint" {
  value       = digitalocean_spaces_bucket.static.bucket_domain_name
  description = "The endpoint for the static files bucket"
}

output "nameservers" {
  value       = digitalocean_domain.default.nameservers
  description = "Nameservers for the domain"
}
