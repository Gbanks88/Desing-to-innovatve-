#!/bin/bash

# Install monitoring tools
apt-get update
apt-get install -y \
    netdata \
    prometheus-node-exporter \
    htop \
    iotop \
    fail2ban

# Configure Netdata
cat > /etc/netdata/netdata.conf << EOF
[global]
    memory mode = dbengine
    page cache size = 32
    dbengine multihost disk space = 256

[web]
    mode = static-threaded
    # Bind to localhost only
    bind to = 127.0.0.1
EOF

# Set up Fail2ban
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = %(sshd_log)s
maxretry = 3
EOF

# Create monitoring script
cat > /usr/local/bin/system_monitor.sh << 'EOF'
#!/bin/bash

# Directory for logs
LOG_DIR="/var/log/system_monitor"
mkdir -p $LOG_DIR

# Thresholds
DISK_THRESHOLD=80
MEM_THRESHOLD=90
CPU_THRESHOLD=90

# Check disk usage
check_disk() {
    df -h / | awk -v threshold=$DISK_THRESHOLD '
        NR==2 {
            gsub(/%/,"",$5)
            if ($5 > threshold) {
                print "ALERT: Disk usage is at " $5 "%"
            }
        }'
}

# Check memory usage
check_memory() {
    free | awk -v threshold=$MEM_THRESHOLD '
        NR==2 {
            total=$2
            used=$3
            pct=used/total*100
            if (pct > threshold) {
                print "ALERT: Memory usage is at " pct "%"
            }
        }'
}

# Check CPU usage
check_cpu() {
    top -bn1 | awk -v threshold=$CPU_THRESHOLD '
        NR==3 {
            cpu=100-$8
            if (cpu > threshold) {
                print "ALERT: CPU usage is at " cpu "%"
            }
        }'
}

# Main monitoring loop
while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    {
        echo "=== System Check: $timestamp ==="
        check_disk
        check_memory
        check_cpu
        echo ""
    } >> "$LOG_DIR/system_monitor.log"
    
    # Rotate log if too large
    if [ $(stat -f%z "$LOG_DIR/system_monitor.log") -gt 10485760 ]; then # 10MB
        mv "$LOG_DIR/system_monitor.log" "$LOG_DIR/system_monitor.log.old"
    fi
    
    sleep 300 # Check every 5 minutes
done
EOF

# Make script executable
chmod +x /usr/local/bin/system_monitor.sh

# Create systemd service for monitoring
cat > /etc/systemd/system/system_monitor.service << EOF
[Unit]
Description=System Resource Monitor
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/system_monitor.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start and enable services
systemctl daemon-reload
systemctl enable --now netdata
systemctl enable --now prometheus-node-exporter
systemctl enable --now fail2ban
systemctl enable --now system_monitor

# Set up log rotation
cat > /etc/logrotate.d/system_monitor << EOF
/var/log/system_monitor/system_monitor.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 root root
}
EOF

echo "Monitoring setup complete!"
echo "Access Netdata dashboard at: http://localhost:19999"
echo "System monitoring logs at: /var/log/system_monitor/system_monitor.log"
