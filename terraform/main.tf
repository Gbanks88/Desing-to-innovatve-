terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Set the DigitalOcean token
provider "digitalocean" {
  token = var.do_token
}

# Create a new Web Droplet in the sf3 region
resource "digitalocean_droplet" "web" {
  image     = "ubuntu-22-04-x64"
  name      = "johnallens-prod"
  region    = "sfo3"
  size      = "s-1vcpu-1gb"
  backups   = true
  monitoring = true
  ssh_keys  = [digitalocean_ssh_key.default.fingerprint]

  tags = ["production", "web"]
}

# Create a new SSH key
resource "digitalocean_ssh_key" "default" {
  name       = "JohnAllens SSH Key"
  public_key = file(var.ssh_public_key_path)
}

# Create a Project
resource "digitalocean_project" "johnallens" {
  name        = "JohnAllens Fashion"
  description = "Fashion Technology Platform"
  purpose     = "Web Application"
  environment = "Production"
  resources   = [digitalocean_droplet.web.urn]
}

# Create a domain
resource "digitalocean_domain" "default" {
  name = "johnallens.com"
}

# Add domain records
resource "digitalocean_record" "www" {
  domain = digitalocean_domain.default.name
  type   = "A"
  name   = "www"
  value  = digitalocean_droplet.web.ipv4_address
}

resource "digitalocean_record" "api" {
  domain = digitalocean_domain.default.name
  type   = "A"
  name   = "api"
  value  = digitalocean_droplet.web.ipv4_address
}

resource "digitalocean_record" "admin" {
  domain = digitalocean_domain.default.name
  type   = "A"
  name   = "admin"
  value  = digitalocean_droplet.web.ipv4_address
}

resource "digitalocean_record" "cdn" {
  domain = digitalocean_domain.default.name
  type   = "A"
  name   = "cdn"
  value  = digitalocean_droplet.web.ipv4_address
}

# Create Spaces bucket for static files
resource "digitalocean_spaces_bucket" "static" {
  name   = "johnallens-static"
  region = "sfo3"
  acl    = "public-read"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*.johnallens.com"]
    max_age_seconds = 3600
  }

  lifecycle_rule {
    enabled = true
    expiration {
      days = 90
    }
  }
}
