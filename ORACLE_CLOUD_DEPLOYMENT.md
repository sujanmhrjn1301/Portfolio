# 🚀 Complete Oracle Cloud Deployment Guide

**Estimated time**: 2-3 hours start to finish

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Oracle Cloud Account Setup](#phase-1-oracle-cloud-account-setup)
3. [Phase 2: Network & Security Setup](#phase-2-network--security-setup)
4. [Phase 3: Create Compute Instance](#phase-3-create-compute-instance)
5. [Phase 4: Connect to Instance](#phase-4-connect-to-instance)
6. [Phase 5: Install Docker](#phase-5-install-docker)
7. [Phase 6: Domain & DNS Setup](#phase-6-domain--dns-setup)
8. [Phase 7: SSL Certificate](#phase-7-ssl-certificate)
9. [Phase 8: Deploy Application](#phase-8-deploy-application)
10. [Phase 9: Monitoring & Maintenance](#phase-9-monitoring--maintenance)

---

## Prerequisites

### What You Need
- [x] Oracle Cloud account (free tier available at https://oracle.com/cloud/free)
- [x] Your portfolio repository cloned locally
- [x] SSH key pair (we'll create this)
- [x] Domain name ($10-15/year at GoDaddy/Namecheap)
- [x] OpenRouter API key (from https://openrouter.ai)
- [x] 30 minutes to 2 hours

### Free Tier Eligible
✅ Oracle Cloud free tier includes enough resources for this project

---

## Phase 1: Oracle Cloud Account Setup

### Step 1.1: Create Oracle Cloud Account

1. Go to https://oracle.com/cloud/free
2. Click "Start for free"
3. Choose region closest to you
4. Enter email and create account
5. Verify email
6. Enter phone number
7. Create password
8. Accept terms

**Time: ~5 minutes**

### Step 1.2: Access Oracle Cloud Console

1. Log in to https://www.oracle.com/cloud/sign-in
2. You should see the Oracle Cloud console dashboard
3. Note your **Tenancy OCID** (shown in top right, looks like: `ocid1.tenancy.oc1..aaaaaa...`)

✅ **Checkpoint**: You have access to Oracle Cloud console

---

## Phase 2: Network & Security Setup

### Step 2.1: Create Virtual Cloud Network (VCN)

1. In Oracle console, click the **hamburger menu** (☰) top left
2. Go to **Networking → Virtual Cloud Networks**
3. Click **Start VCN Wizard**
4. Choose **VCN with Internet Connectivity**
5. Click **Start VCN Wizard**

Fill in:
- **VCN Name**: `portfolio-vcn`
- **VCN CIDR Block**: `10.0.0.0/16` (default)
- **Public Subnet CIDR Block**: `10.0.1.0/24` (default)
- **Private Subnet CIDR Block**: Leave default (we won't use it)

6. Click **Next**
7. Click **Create**

**Wait**: ~2-3 minutes for VCN to create

✅ **Checkpoint**: VCN created

### Step 2.2: Configure Security List (Firewall)

1. Go to **Networking → Virtual Cloud Networks**
2. Click on your VCN `portfolio-vcn`
3. Click **Security Lists** in left menu
4. Click **Default Security List for portfolio-vcn**
5. Click **Add Ingress Rules** (add 3 rules)

**Rule 1 - SSH Access:**
- Source: Your IP (find at https://ipinfo.io)
  - Or use: `0.0.0.0/0` (anyone, less secure)
- Protocol: TCP
- Destination Port Range: `22`
- Description: OS SSH

Click **Add Ingress Rule**

**Rule 2 - HTTP:**
- Source: `0.0.0.0/0`
- Protocol: TCP
- Destination Port Range: `80`
- Description: HTTP

Click **Add Ingress Rule**

**Rule 3 - HTTPS:**
- Source: `0.0.0.0/0`
- Protocol: TCP
- Destination Port Range: `443`
- Description: HTTPS

Click **Add Ingress Rule**

✅ **Checkpoint**: Security rules configured

---

## Phase 3: Create Compute Instance

### Step 3.1: Create Instance

1. Click **hamburger menu** (☰)
2. Go to **Compute → Instances**
3. Make sure correct compartment is selected (top left dropdown)
4. Click **Create Instance**

Fill in:

**Image and shape:**
- **Image**: Click **Change Image**
  - Select **Canonical Ubuntu 22.04**
  - Click **Select Image**
- **Shape**: Click **Change Shape** (if needed)
  - Select **Ampere (ARM)** (cheaper for free tier)
  - Shape: `VM.Standard.A1.Flex`
  - Ocpus: `1` (free tier allows 4)
  - RAM: `6` (free tier allows 24 GB)
  - Click **Select Shape**

**Networking:**
- VCN: `portfolio-vcn`
- Subnet: `Public Subnet-portfolio-vcn`
- Public IPv4: Check **Assign a public IPv4 address**

**SSH key:**
- Click **Generate a key pair for me**
- This downloads `ssh-key-2024-04-08.key`
- **SAVE THIS FILE SECURELY** (you'll need it to connect)

6. Scroll down, click **Create**

**Wait**: ~2-3 minutes for instance to create

✅ **Checkpoint**: Instance running

### Step 3.2: Note Your Instance Details

1. Go to **Compute → Instances**
2. Click on your instance
3. Copy and save:
   - **Public IP Address** (e.g., `152.70.xyz.abc`)
   - **Instance OCID** (backup in case you need it)

---

## Phase 4: Connect to Instance

### Step 4.1: Prepare SSH Key

**On Windows (PowerShell):**

```powershell
# Navigate to where you saved the key
cd $env:USERPROFILE\Downloads

# Set permissions (required for SSH)
icacls "ssh-key-2024-04-08.key" /inheritance:r /grant:r "%username%:F"

# Or use WSL/Git Bash:
chmod 600 ssh-key-2024-04-08.key
```

**On Mac/Linux:**
```bash
cd ~/Downloads
chmod 600 ssh-key-2024-04-08.key
```

### Step 4.2: Connect via SSH

**On Windows (PowerShell or Git Bash):**
```bash
ssh -i ssh-key-2024-04-08.key ubuntu@YOUR_PUBLIC_IP
```

**On Mac/Linux:**
```bash
ssh -i ~/Downloads/ssh-key-2024-04-08.key ubuntu@YOUR_PUBLIC_IP
```

Replace `YOUR_PUBLIC_IP` with your instance IP (from Step 3.2)

**First time connecting?**
- Type `yes` when asked "Are you sure?"

✅ **Checkpoint**: Connected to instance

---

## Phase 5: Install Docker

### Step 5.1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

**Time**: ~2 minutes

### Step 5.2: Install Docker

```bash
# Download Docker installer
curl -fsSL https://get.docker.com -o get-docker.sh

# Run installer
sudo sh get-docker.sh

# Add user to docker group (no sudo needed)
sudo usermod -aG docker ubuntu

# Exit and reconnect
exit
```

Reconnect:
```bash
ssh -i ssh-key-2024-04-08.key ubuntu@YOUR_PUBLIC_IP
```

### Step 5.3: Install Docker Compose

```bash
# Latest Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

Should show: `Docker Compose version 2.x.x`

✅ **Checkpoint**: Docker installed

---

## Phase 6: Domain & DNS Setup

### Step 6.1: Buy Domain (5 minutes)

Choose one:
- **GoDaddy** (https://godaddy.com)
- **Namecheap** (https://namecheap.com)
- **Cloudflare** (https://cloudflare.com)

1. Search for domain
2. Add to cart
3. Make payment
4. Note your domain name (e.g., `sujanmaharjan.com`)

### Step 6.2: Point DNS to Oracle Instance

**If using GoDaddy:**

1. Go to GoDaddy dashboard
2. Select your domain
3. Click **DNS** or **Manage DNS**
4. Find **A Record**
5. Edit A record:
   - **Points to**: `YOUR_PUBLIC_IP`
   - Click **Save**

**If using Namecheap:**

1. Go to Namecheap dashboard
2. Click **Manage** next to domain
3. Click **Advanced DNS**
4. Find A record (@ symbol)
5. Edit:
   - **Value**: `YOUR_PUBLIC_IP`
   - Click **Save**

**If using Cloudflare:**

1. Add your domain to Cloudflare
2. Update nameservers at registrar
3. Go to DNS records
4. Add A record:
   - **Name**: `@`
   - **IPv4**: `YOUR_PUBLIC_IP`
   - **Proxy**: DNS only (gray cloud)
   - **Save**

### Step 6.3: Verify DNS Propagation

```bash
# On your local computer
nslookup yourdomain.com
# or
dig yourdomain.com
```

Should show your Oracle instance IP

**Time for DNS to propagate**: 1-24 hours (usually 5-30 minutes)

✅ **Checkpoint**: Domain points to your instance

---

## Phase 7: SSL Certificate

### Step 7.1: Install Certbot

On your **Oracle instance**:

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
```

### Step 7.2: Get SSL Certificate

```bash
# Get certificate (replace with your domain)
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  -m your-email@example.com \
  --agree-tos \
  --non-interactive
```

**What happens:**
- Certbot validates you own the domain
- Creates certificate files
- Saves to `/etc/letsencrypt/live/yourdomain.com/`

### Step 7.3: Copy Certificates for Application

```bash
# Create directory for certificates
mkdir -p ~/Portfolio/nginx/ssl

# Copy certificates (replace yourdomain.com)
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ~/Portfolio/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ~/Portfolio/nginx/ssl/key.pem

# Fix permissions
sudo chown ubuntu:ubuntu ~/Portfolio/nginx/ssl/*.pem
```

✅ **Checkpoint**: SSL certificates ready

---

## Phase 8: Deploy Application

### Step 8.1: Clone Repository

```bash
# Clone your GitHub repo
git clone https://github.com/sujanmhrjn1301/Portfolio.git
cd Portfolio
```

### Step 8.2: Create Production Environment File

```bash
# Copy template
cp .env.production.example .env

# Edit with your values
nano .env
```

**In nano editor**, add your values:

```bash
# ============ CRITICAL SECURITY ============
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=generate-using-this-command-below
API_KEY=generate-using-this-command-below

# ============ API KEYS ============
OPENROUTER_API_KEY=sk-or-v1-YOUR_ACTUAL_KEY
GITHUB_TOKEN=

# ============ CORS ============
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# ============ DATABASE ============
CHAT_DB_PATH=/var/lib/portfolio/chat_history.db
CHROMA_DB_PATH=/var/lib/portfolio/chroma_db

# ============ PORTFOLIO INFO ============
PORTFOLIO_NAME=Your Name
PORTFOLIO_GITHUB=https://github.com/yourusername
PORTFOLIO_LINKEDIN=https://linkedin.com/in/yourprofile
PORTFOLIO_EMAIL=contact@yourdomain.com
PORTFOLIO_PHONE=
PORTFOLIO_LOCATION=

# ============ FRONTEND ============
REACT_APP_API_URL=https://yourdomain.com
```

**To generate SECRET_KEY and API_KEY**, run in another terminal window:

```bash
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python3 -c "import secrets; print('API_KEY=' + secrets.token_urlsafe(32))"
```

Copy the output into your .env file.

**Save nano:**
- Press `Ctrl+X`
- Type `Y`
- Press `Enter`

### Step 8.3: Update nginx Configuration

Edit the domain in nginx config:

```bash
nano nginx/nginx.conf
```

Find the line:
```
server_name _;
```

Replace with:
```
server_name yourdomain.com www.yourdomain.com;
```

Save: `Ctrl+X`, `Y`, `Enter`

### Step 8.4: Build and Start Services

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Wait 30 seconds for services to start
sleep 30

# Check status
docker-compose -f docker-compose.prod.yml ps
```

All should show `Up`

### Step 8.5: Verify Deployment

```bash
# Check logs for errors
docker-compose -f docker-compose.prod.yml logs

# Test health endpoint
curl https://yourdomain.com/health

# Should return: {"status": "ok", "environment": "production", "version": "2.0.0"}
```

✅ **Checkpoint**: Application deployed and running

---

## Phase 9: Monitoring & Maintenance

### Step 9.1: View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Just backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Just frontend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Just nginx
docker-compose -f docker-compose.prod.yml logs -f nginx

# Last 50 lines
docker-compose -f docker-compose.prod.yml logs --tail=50
```

### Step 9.2: Monitor Resources

```bash
# See CPU/Memory usage
docker stats
```

### Step 9.3: SSL Certificate Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Set up automatic renewal (cron job)
sudo crontab -e

# Add this line (renew daily at 3 AM):
0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /home/ubuntu/Portfolio/nginx/ssl/cert.pem && cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /home/ubuntu/Portfolio/nginx/ssl/key.pem && docker-compose -f /home/ubuntu/Portfolio/docker-compose.prod.yml restart nginx
```

### Step 9.4: Regular Backups

Create backup script:

```bash
cat > ~/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/ubuntu/Portfolio/backups"
mkdir -p $BACKUP_DIR

# Backup database
docker-compose -f ~/Portfolio/docker-compose.prod.yml exec backend \
  cp /var/lib/portfolio/chat_history.db \
  $BACKUP_DIR/chat_history_$(date +%Y%m%d_%H%M%S).db

# Backup chroma data
docker-compose -f ~/Portfolio/docker-compose.prod.yml exec backend \
  tar -czf $BACKUP_DIR/chroma_$(date +%Y%m%d).tar.gz \
  /var/lib/portfolio/chroma_db

echo "Backup completed at $(date)"
EOF

# Make executable
chmod +x ~/backup.sh

# Run daily at 2 AM
crontab -e
# Add: 0 2 * * * /home/ubuntu/backup.sh
```

### Step 9.5: Monitor with Uptime Monitoring

Use a free service like:
- **Uptime Robot** (https://uptimerobot.com)
- **Pingdom** (https://pingdom.com)

1. Sign up
2. Add URL: `https://yourdomain.com/health`
3. Alert if down

### Step 9.6: Check for Updates

Monthly:
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🎯 Testing Your Deployment

### Test 1: Frontend Loads
```bash
curl -I https://yourdomain.com
# Should show: HTTP/1.1 200 OK
```

### Test 2: API Responds
```bash
curl https://yourdomain.com/api/health
# Should show: {"status":"ok",...}
```

### Test 3: Chat Works
Open browser:
```
https://yourdomain.com
```
- Wait for page to load
- Type a message in chat
- Should see response from AI

### Test 4: Rate Limiting
```bash
# Rapid requests
for i in {1..20}; do
  curl https://yourdomain.com/api/chat
done
# Some should return 429 (rate limited)
```

### Test 5: SSL Certificate
```bash
# Check certificate validity
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | grep -A 2 "Verify return code"
# Should show: Verify return code: 0 (ok)
```

---

## 🚨 Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Common issues:
# 1. Port already in use
docker-compose -f docker-compose.prod.yml down

# 2. Out of memory
docker stats

# 3. Missing .env file
ls -la .env
```

### 502 Bad Gateway
```bash
# Backend is down, check:
docker-compose -f docker-compose.prod.yml logs backend

# Restart
docker-compose -f docker-compose.prod.yml restart backend
```

### SSL Certificate Issues
```bash
# Check certificate
openssl x509 -in ~/Portfolio/nginx/ssl/cert.pem -text -noout | grep -A 2 "Valid"

# Get new certificate
sudo certbot certonly --standalone -d yourdomain.com --force-renewal
```

### Out of Disk Space
```bash
# Check usage
df -h

# Clean up Docker
docker system prune -a

# Remove old backups
cd ~/Portfolio/backups && rm -f *.db *.tar.gz
```

---

## 📊 Monitoring Dashboard

Once deployed, monitor:

1. **Application Health**
   - Visit: `https://yourdomain.com/health`
   - Should show: `{"status":"ok"}`

2. **Resource Usage**
   - SSH into instance
   - Run: `docker stats`

3. **Error Logs**
   - SSH into instance
   - Run: `docker-compose -f docker-compose.prod.yml logs -f backend`

4. **Rate Limiting**
   - Test: `for i in {1..150}; do curl https://yourdomain.com/api/chat; done`
   - Some should return 429

---

## 🎓 Common Commands Reference

```bash
# Connect to instance
ssh -i ssh-key.key ubuntu@YOUR_IP

# View all services
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Stop services
docker-compose -f docker-compose.prod.yml down

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Update and restart
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# View resource usage
docker stats

# Check disk space
df -h

# Check certificate expiry
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | grep -A 2 "notAfter"
```

---

## ✅ Deployment Complete!

You now have:
- ✅ Production-grade AI portfolio
- ✅ Secure with JWT authentication
- ✅ Rate limiting & input validation
- ✅ SSL/TLS encrypted
- ✅ Auto-renewable certificates
- ✅ Daily backups
- ✅ Monitoring & alerts

**Your portfolio is live at**: `https://yourdomain.com`

---

## 📞 Support & Questions

If you encounter issues:

1. Check logs: `docker-compose logs`
2. Review: `DEPLOYMENT_SECURITY.md`
3. Check: `SECURITY.md`
4. SSH and debug manually

---

**Deployed on**: April 8, 2026  
**Status**: 🟢 **PRODUCTION LIVE**
