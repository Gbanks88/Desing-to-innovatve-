# DNS Configuration Guide for johnallens.com

## Domain Registrar Setup

### A Records
```
Record Type | Name    | Value             | TTL
-----------|---------|-------------------|-----
A          | @       | [SERVER_IP]       | 3600
A          | www     | [SERVER_IP]       | 3600
A          | api     | [API_SERVER_IP]   | 3600
A          | admin   | [ADMIN_SERVER_IP] | 3600
A          | cdn     | [CDN_SERVER_IP]   | 3600
```

### CNAME Records
```
Record Type | Name    | Value            | TTL
-----------|---------|------------------|-----
CNAME      | www     | johnallens.com.  | 3600
```

### MX Records
```
Record Type | Name    | Value                | Priority | TTL
-----------|---------|---------------------|----------|-----
MX         | @       | mail.johnallens.com | 10       | 3600
```

### TXT Records
```
Record Type | Name    | Value                                    | TTL
-----------|---------|----------------------------------------|-----
TXT        | @       | v=spf1 include:_spf.johnallens.com ~all | 3600
```

### CAA Records
```
Record Type | Name    | Value                                  | TTL
-----------|---------|----------------------------------------|-----
CAA        | @       | 0 issue "letsencrypt.org"              | 3600
CAA        | @       | 0 issuewild "letsencrypt.org"         | 3600
```

## Security Records

### DMARC Record
```
Record Type | Name          | Value                                                            | TTL
-----------|---------------|----------------------------------------------------------------|-----
TXT        | _dmarc        | v=DMARC1; p=reject; rua=mailto:dmarc@johnallens.com            | 3600
```

### DKIM Record
```
Record Type | Name          | Value                                                            | TTL
-----------|---------------|----------------------------------------------------------------|-----
TXT        | default._domainkey | v=DKIM1; k=rsa; p=[YOUR_PUBLIC_KEY]                       | 3600
```

## Step-by-Step Setup Instructions

1. Log into your domain registrar's control panel
2. Navigate to the DNS management section
3. Add each record as specified above
4. For each [SERVER_IP] placeholder, use your actual server IP addresses
5. Wait for DNS propagation (can take up to 48 hours)

## Verification Steps

1. Use dig or nslookup to verify A records:
   ```
   dig johnallens.com
   dig www.johnallens.com
   dig api.johnallens.com
   dig admin.johnallens.com
   dig cdn.johnallens.com
   ```

2. Verify CNAME record:
   ```
   dig www.johnallens.com CNAME
   ```

3. Verify MX records:
   ```
   dig johnallens.com MX
   ```

4. Verify TXT records:
   ```
   dig johnallens.com TXT
   ```

## Common DNS Propagation Check Tools

- https://www.whatsmydns.net
- https://dnschecker.org
- https://mxtoolbox.com

## Troubleshooting

1. If DNS records are not propagating:
   - Verify TTL values are correct
   - Clear local DNS cache
   - Try different DNS servers

2. If SSL verification fails:
   - Ensure A records are properly configured
   - Wait for DNS propagation
   - Verify no CAA records are blocking Let's Encrypt

3. If email is not working:
   - Verify MX records
   - Check SPF, DKIM, and DMARC records
   - Verify mail server configuration
