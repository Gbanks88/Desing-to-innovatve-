# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "unix:/tmp/gunicorn.sock"  # Unix socket
# bind = "127.0.0.1:8000"         # Alternative: TCP socket

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'

# Process naming
proc_name = 'johnallens_backend'

# SSL (if not using Nginx)
# keyfile = '/etc/letsencrypt/live/johnallens.com/privkey.pem'
# certfile = '/etc/letsencrypt/live/johnallens.com/fullchain.pem'
