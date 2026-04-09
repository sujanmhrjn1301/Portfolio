# 🚀 Deployment & Security Setup Guide

This guide covers production deployment with all security measures in place.

---

## Environment Setup for Production

### 1. Backend Environment Variables

Create `.env` in `backend/` with **real production values**:

```bash
# ============ CRITICAL SECURITY ============
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=generate-using: python -c "import secrets; print(secrets.token_urlsafe(32))"

# ============ API KEYS (from your accounts) ============
OPENROUTER_API_KEY=sk-or-v1-your-production-key-here
GITHUB_TOKEN=ghp_your-production-token
API_KEY=generate-using: python -c "import secrets; print(secrets.token_urlsafe(32))"

# ============ CORS (your domain only) ============
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# ============ DATABASE ============
# Default: ./chat_history.db (SQLite)
# For production, consider using PostgreSQL or encrypted SQLite
CHAT_DB_PATH=/var/lib/portfolio/chat_history.db
CHROMA_DB_PATH=/var/lib/portfolio/chroma_db

# ============ LOGGING ============
LOG_LEVEL=INFO

# ============ PORTFOLIO INFO (optional, non-sensitive) ============
PORTFOLIO_NAME=Your Name
PORTFOLIO_GITHUB=https://github.com/yourusername
PORTFOLIO_LINKEDIN=https://linkedin.com/in/yourprofile
# Keep these empty in production
PORTFOLIO_PHONE=
PORTFOLIO_EMAIL=contact@yourdomain.com
```

### 2. Frontend Environment Variables

Create `.env` in `frontend/`:

```bash
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_AUTH_TOKEN=
```

---

## Docker Compose for Production

### Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: portfolio_backend_prod
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - API_KEY=${API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - CORS_ORIGINS=${CORS_ORIGINS}
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
    volumes:
      - backend_data:/app/data
      - backend_chroma:/app/chroma_db
      - backend_db:/app/chat_history.db
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - portfolio_network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: portfolio_frontend_prod
    environment:
      - REACT_APP_API_URL=https://api.yourdomain.com
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: always
    networks:
      - portfolio_network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    container_name: portfolio_nginx_prod
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./frontend/build:/usr/share/nginx/html:ro
    depends_on:
      - backend
      - frontend
    restart: always
    networks:
      - portfolio_network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  backend_data:
  backend_chroma:
  backend_db:

networks:
  portfolio_network:
    driver: bridge
```

### Run Production:

```bash
# Load environment variables
export $(cat .env | xargs)

# Start with production compose file
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Health check
curl https://yourdomain.com/health
```

---

## Nginx Reverse Proxy Setup

### Create `nginx/nginx.conf`:

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 1M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=5r/s;

    # Upstream backends
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL certificates (get from Let's Encrypt)
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # HSTS
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Root location (frontend)
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
        }

        # API routes
        location /api/ {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://backend/;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_buffering off;
            proxy_request_buffering off;
        }

        # Static files cache
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Health check endpoint
        location /health {
            proxy_pass http://backend;
            access_log off;
        }
    }
}
```

### SSL Certificate Setup (Let's Encrypt):

```bash
# Install Certbot
apt-get install certbot python3-certbot-nginx

# Get certificate
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy to nginx directory
mkdir -p nginx/ssl
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem

# Auto-renewal
certbot renew --quiet --no-eff-email
```

---

## Security Hardening Checklist

### Before Going Live

- [ ] All environment variables set in `.env`
- [ ] `SECRET_KEY` is cryptographically strong
- [ ] `DEBUG=false` in production
- [ ] `ENVIRONMENT=production`
- [ ] CORS origins restricted to your domain(s)
- [ ] HTTPS/TLS certificate installed and valid
- [ ] `nginx.conf` using restrictive security headers
- [ ] Rate limiting configured in nginx and FastAPI
- [ ] Database backups automated
- [ ] Logging configured and monitored
- [ ] API keys have minimal required scope
- [ ] No secrets in Docker images
- [ ] Docker containers run as non-root user
- [ ] Health checks configured
- [ ] Monitoring and alerting set up

### Ongoing Security

- [ ] Regularly update dependencies (`pip list --outdated`)
- [ ] Monitor logs for suspicious activity
- [ ] Review rate limit metrics
- [ ] Test disaster recovery procedures monthly
- [ ] Rotate API keys quarterly
- [ ] Review SSL certificate expiration dates
- [ ] Check for security advisories weekly

---

## Monitoring & Logging

### View Logs:

```bash
# Backend logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Nginx logs
docker-compose -f docker-compose.prod.yml logs -f nginx

# Combined
docker-compose -f docker-compose.prod.yml logs -f

# With timestamps
docker-compose -f docker-compose.prod.yml logs -f --timestamps
```

### Metrics to Monitor

```bash
# API health
curl https://yourdomain.com/health

# Response times
curl -w "@curl-format.txt" https://yourdomain.com/api/health

# Rate limit status
curl -i https://yourdomain.com/api/chat

# Check response headers:
# X-RateLimit-Limit
# X-RateLimit-Remaining
# X-RateLimit-Reset
```

---

## Backup Strategy

### Database Backup:

```bash
# Automated daily backup
0 2 * * * docker-compose -f docker-compose.prod.yml exec backend \
  bash -c 'cp /app/chat_history.db /app/backups/chat_history_$(date +%Y%m%d).db'

# Backup chroma data
0 2 * * * docker-compose -f docker-compose.prod.yml exec backend \
  bash -c 'tar -czf /app/backups/chroma_$(date +%Y%m%d).tar.gz /app/chroma_db'

# Upload to S3/Cloud Storage
aws s3 sync /app/backups s3://your-backup-bucket/portfolio/
```

---

## Disaster Recovery

### If Compromise Suspected:

```bash
# 1. Stop services
docker-compose -f docker-compose.prod.yml down

# 2. Rotate all secrets
# Update .env with new API keys

# 3. Restart
docker-compose -f docker-compose.prod.yml up -d

# 4. Review logs
docker-compose -f docker-compose.prod.yml logs --since 1h backend
```

### If Database Corrupted:

```bash
# 1. Restore from latest backup
cp /backups/chat_history_20260408.db data/chat_history.db
cp -r /backups/chroma_20260408 data/chroma_db

# 2. Restart backend
docker-compose -f docker-compose.prod.yml restart backend
```

---

## Performance Optimization

### Nginx Caching:

```nginx
# Cache static assets for 1 year
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Don't cache HTML
location ~* \.html$ {
    expires 1h;
    add_header Cache-Control "public, must-revalidate";
}
```

### FastAPI Optimization:

```python
# In config.py
UVICORN_WORKERS = 4  # Adjust based on CPU cores
UVICORN_BACKLOG = 2048
```

---

## Troubleshooting

### 503 Service Unavailable

```bash
# Check backend health
curl http://localhost:8000/health

# Check docker status
docker-compose -f docker-compose.prod.yml ps

# View backend logs
docker-compose -f docker-compose.prod.yml logs backend
```

### High Memory Usage

```bash
# Check container resources
docker stats

# Restart container
docker-compose -f docker-compose.prod.yml restart backend
```

### SSL Certificate Issues

```bash
# Test certificate
openssl s_client -connect yourdomain.com:443

# Check expiration
openssl x509 -enddate -noout -in nginx/ssl/cert.pem

# Renew certificate
certbot renew
```

---

## Support & Questions

For security or deployment issues:
- Check logs: `docker-compose logs -f`
- Review SECURITY.md
- Test in development first
- Email: `security@example.com`

---

**Last Updated**: April 8, 2026  
**Version**: 2.0 (Production-Ready)
