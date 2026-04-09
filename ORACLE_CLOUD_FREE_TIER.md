# 🎉 Oracle Cloud Free Tier Deployment Guide

**For Free Trial Account Only**  
**Estimated time**: 1.5-2 hours

---

## Free Tier Resources Available

### ✅ You Get (Always Free)

| Resource | Amount | What You Use |
|----------|--------|--------------|
| Compute Instances | 2 AMD OR 4 ARM | **1 ARM (best for portfolio)** |
| vCPU/RAM | 1 OCPU + 6GB RAM | Perfect for portfolio |
| Storage | 200 GB | Database + app data |
| Object Storage | 10 GB | Backups |
| Outbound Data | 10 GB/month | Website traffic |
| Load Balancer | 1 free | Optional |

### 💰 You Also Get (First 30 Days)

- $300 in free credits
- Can use for additional resources/testing

### ❌ What You Won't Use

- Additional compute instances (stay within free tier)
- Database VM (use storage instead)
- Additional VCNs (stick with 1)

---

## Architecture for Free Tier

```
┌─────────────────────────────┐
│   Your Domain (GoDaddy)     │
│   yourdomain.com            │
└──────────────┬──────────────┘
               │ DNS Points to
               ▼
┌─────────────────────────────┐
│   Oracle Cloud Instance     │
│   Ubuntu 22.04 ARM (Free)   │
│   1 OCPU + 6GB RAM          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Docker Containers         │
│  ├─ Backend (FastAPI)       │
│  ├─ Frontend (React)        │
│  └─ Nginx Reverse Proxy     │
└─────────────────────────────┘
```

---

## Table of Contents

1. [Free Tier Setup](#free-tier-setup)
2. [Network Configuration](#network-configuration)
3. [Create Free Tier Instance](#create-free-tier-instance)
4. [Connect to Instance](#connect-to-instance)
5. [Install Docker](#install-docker)
6. [Domain & DNS](#domain--dns)
7. [SSL Certificate](#ssl-certificate)
8. [Deploy Application](#deploy-application)
9. [Free Tier Monitoring](#free-tier-monitoring)

---

## Free Tier Setup

### Step 1: Access Always Free Dashboard

1. Log in to https://www.oracle.com/cloud/sign-in
2. Click **Console** (top right)
3. You're in your free tier account

### Step 2: Check Free Tier Resources

1. Click **hamburger menu** (☰) top left
2. Go to **Governance & Administration → Limits, Quotas and Usage**
3. Check your **Compute** resources
   - You should see: **2 AMD or 4 Ampere instances**
   - We'll use 1 Ampere (best for portfolio)

✅ **Checkpoint**: You have free tier resources available

---

## Network Configuration

### Step 3: Create Virtual Cloud Network (VCN)

1. Click **hamburger menu** (☰)
2. Go to **Networking → Virtual Cloud Networks**
3. Click **Create VCN**

Fill in:
- **VCN Name**: `portfolio-free-vcn`
- **Compartment**: (default)
- **VCN CIDR Block**: `10.0.0.0/16`
- Leave other settings as default

4. Click **Create VCN**

**Wait**: ~1 minute

✅ **Checkpoint**: VCN created

### Step 4: Create Subnet

1. Go to your VCN `portfolio-free-vcn`
2. Click **Subnets** in left menu
3. Click **Create Subnet**

Fill in:
- **Name**: `public-subnet-1`
- **Subnet CIDR Block**: `10.0.1.0/24`
- **Route Table**: Select the route table with IGW
- Keep other defaults

4. Click **Create Subnet**

✅ **Checkpoint**: Subnet created

### Step 5: Configure Security (Firewall Rules)

1. Go to your VCN
2. Click **Security Lists** in left menu
3. Click **Default Security List**
4. Click **Add Ingress Rules**

**Add Rule 1 - SSH (Port 22):**
- Source CIDR: `0.0.0.0/0`
- Protocol: TCP
- Source Port Range: (empty)
- Destination Port Range: `22`
- Description: `SSH Access`
- Click **Add Ingress Rule**

**Add Rule 2 - HTTP (Port 80):**
- Source CIDR: `0.0.0.0/0`
- Protocol: TCP
- Destination Port Range: `80`
- Description: `HTTP`
- Click **Add Ingress Rule**

**Add Rule 3 - HTTPS (Port 443):**
- Source CIDR: `0.0.0.0/0`
- Protocol: TCP
- Destination Port Range: `443`
- Description: `HTTPS`
- Click **Add Ingress Rule**

✅ **Checkpoint**: Firewall configured

---

## Create Free Tier Instance

### Step 6: Create Compute Instance

1. Click **hamburger menu** (☰)
2. Go to **Compute → Instances**
3. Click **Create Instance**

**Name and Image:**
- **Instance Name**: `portfolio-free-instance`
- **Image**: Click **Change Image** 
  - Search for: `Ubuntu 22.04`
  - Select **Canonical Ubuntu 22.04 - Arm64 (aarch64)**
  - Click **Select Image**

**Shape (IMPORTANT for free tier):**
- Click **Change Shape**
- Select **Ampere (Arm)**
- Select **VM.Standard.A1.Flex**
  - **OCPU Count**: `1` (minimum, free tier allows 4)
  - **RAM Amount in GB**: `6` (free tier allows 24GB)
  - Click **Select Shape**

**Networking:**
- **VCN**: `portfolio-free-vcn`
- **Subnet**: `public-subnet-1`
- Check **Assign a public IPv4 address**

**SSH Key:**
- Click **Generate a key pair for me**
- Click **Download Private Key** (saves as `ssh-key-xxxx.key`)
- **SAVE THIS SECURELY** - you need it to connect!

8. Click **Create**

**Wait**: ~3 minutes for instance to start

✅ **Checkpoint**: Free tier instance running

### Step 7: Get Instance IP

1. Go to **Compute → Instances**
2. Click your instance `portfolio-free-instance`
3. Under **Instance Details**, copy:
   - **Public IP Address** (e.g., `150.x.x.x`)
   - Save this!

---

## Connect to Instance

### Step 8: SSH Connection

**On Windows (PowerShell):**
```powershell
# Set SSH key permissions
icacls "C:\Users\YourName\Downloads\ssh-key-xxxx.key" /inheritance:r /grant:r "%username%:F"

# Connect (replace IP with your instance IP)
ssh -i "C:\Users\YourName\Downloads\ssh-key-xxxx.key" opc@YOUR_INSTANCE_IP
```

**On Mac/Linux:**
```bash
# Make key readable only by you
chmod 600 ~/Downloads/ssh-key-xxxx.key

# Connect
ssh -i ~/Downloads/ssh-key-xxxx.key opc@YOUR_INSTANCE_IP
```

**First time?**
- Type `yes` when asked "Are you sure?"

✅ **Checkpoint**: Connected to instance

---

## Install Docker

### Step 9: Update System

```bash
sudo yum update -y
```

**Time**: ~2 minutes (might be slow on first boot)

### Step 10: Install Docker

```bash
# Download Docker installer
curl -fsSL https://get.docker.com -o get-docker.sh

# Install
sudo sh get-docker.sh

# Add yourself to docker group (no sudo needed)
sudo usermod -aG docker opc

# Exit SSH
exit
```

### Step 11: Reconnect and Verify

```bash
# Reconnect (same SSH command as Step 8)
ssh -i "path/to/ssh-key-xxxx.key" opc@YOUR_INSTANCE_IP

# Verify Docker
docker --version
# Should show: Docker version 24.x.x
```

### Step 12: Install Docker Compose

```bash
# Install latest version
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
# Should show: Docker Compose version 2.x.x
```

✅ **Checkpoint**: Docker ready

---

## Domain & DNS

### Step 13: Buy Domain Name (Free Tier Compatible)

Choose a provider:
- **GoDaddy** (https://godaddy.com) - $0.99 first year
- **Namecheap** (https://namecheap.com) - $0.88 first year
- **Porkbun** (https://porkbun.com) - $0.99 for .com

1. Pick a domain (e.g., `sujanmaharjan.com`)
2. Add to cart
3. Pay
4. Note your domain name

✅ **Checkpoint**: Domain registered

### Step 14: Point Domain to Oracle Instance

**Using GoDaddy:**

1. Log in to GoDaddy
2. Go to **My Products → Domains**
3. Click **Manage DNS** for your domain
4. Find **A Record** (points to: @)
5. Edit:
   - **Points to**: Your Oracle instance IP
   - Click **Save**

**Using Namecheap:**

1. Log in to Namecheap
2. Go to **My Domains**
3. Click **Manage** for your domain
4. Go to **Advanced DNS**
5. Find A record (@)
6. Click **Edit**:
   - **IPv4 Address**: Your Oracle instance IP
   - Click **Save**

### Step 15: Verify DNS

On your **local computer** (not on instance):

```bash
# Windows
nslookup yourdomain.com

# Mac/Linux
dig yourdomain.com
```

Should show your Oracle instance IP

**Wait time**: 5-30 minutes for DNS to propagate

---

## SSL Certificate

### Step 16: Install Certbot

On your **Oracle instance**:

```bash
sudo yum install -y certbot
```

### Step 17: Get Free SSL Certificate

```bash
# Wait for DNS to propagate first!

# Get certificate (replace yourdomain.com)
sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  -m your-email@gmail.com \
  --agree-tos \
  --non-interactive
```

If it fails, DNS hasn't propagated yet - wait 5 more minutes and try again.

### Step 18: Copy Certificates

```bash
# Create directory
mkdir -p ~/Portfolio/nginx/ssl

# Copy (replace yourdomain.com)
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ~/Portfolio/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ~/Portfolio/nginx/ssl/key.pem

# Fix permissions
sudo chown opc:opc ~/Portfolio/nginx/ssl/*.pem

# Verify
ls -la ~/Portfolio/nginx/ssl/
# Should show cert.pem and key.pem
```

✅ **Checkpoint**: SSL certificate ready

---

## Deploy Application

### Step 19: Clone Your Repository

```bash
# Clone from GitHub
git clone https://github.com/sujanmhrjn1301/Portfolio.git
cd Portfolio

# Verify files
ls -la
# Should show: docker-compose.prod.yml, nginx/, backend/, frontend/
```

### Step 20: Create Production .env File

```bash
# Copy template
cp .env.production.example .env

# Edit
nano .env
```

**Paste this** (replace values in ALL_CAPS):

```bash
# ============ SECURITY ============
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=GENERATE_USING_COMMAND_BELOW
API_KEY=GENERATE_USING_COMMAND_BELOW

# ============ API KEYS ============
# Get from https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-YOUR_ACTUAL_KEY_HERE

# Optional GitHub token
GITHUB_TOKEN=

# ============ CORS (IMPORTANT!) ============
# Replace with YOUR domain
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# ============ DATABASE ============
CHAT_DB_PATH=/var/lib/portfolio/chat_history.db
CHROMA_DB_PATH=/var/lib/portfolio/chroma_db

# ============ PORTFOLIO INFO ============
PORTFOLIO_NAME=Your Name Here
PORTFOLIO_GITHUB=https://github.com/yourusername
PORTFOLIO_LINKEDIN=https://linkedin.com/in/yourprofile
PORTFOLIO_EMAIL=your-email@gmail.com
PORTFOLIO_PHONE=
PORTFOLIO_LOCATION=

# ============ FRONTEND ============
# Replace with YOUR domain
REACT_APP_API_URL=https://yourdomain.com
```

**To generate SECRET_KEY and API_KEY**, open a NEW terminal window and run:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run twice, copy both outputs into your .env file

**Save nano:**
- Press `Ctrl+X`
- Type `Y`
- Press `Enter`

### Step 21: Update nginx Configuration

```bash
nano nginx/nginx.conf
```

Find these lines around line 140:
```
server {
    listen 443 ssl http2;
    server_name _;
```

Replace `server_name _;` with:
```
server_name yourdomain.com www.yourdomain.com;
```

**Save:** `Ctrl+X`, `Y`, `Enter`

### Step 22: Build Docker Images

```bash
# Takes ~3-5 minutes on free tier
docker-compose -f docker-compose.prod.yml build
```

### Step 23: Start Application

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Wait 30 seconds
sleep 30

# Check status
docker-compose -f docker-compose.prod.yml ps
```

All should show `Up`

### Step 24: Test Deployment

**Test 1 - Health Check:**
```bash
curl https://yourdomain.com/health
```

Should return:
```json
{"status":"ok","environment":"production","version":"2.0.0"}
```

**Test 2 - API Response:**
```bash
curl https://yourdomain.com/api/portfolio-info
```

Should return your portfolio info

**Test 3 - Open in Browser:**
1. Visit: `https://yourdomain.com`
2. Page should load
3. Try sending a message in chat

✅ **Checkpoint**: Application deployed!

---

## Free Tier Monitoring

### Step 25: Monitor Resource Usage

```bash
# SSH to instance
ssh -i key.pem ubuntu@YOUR_IP

# Check memory (6GB available)
free -h

# Check disk (important on free tier)
df -h

# Watch Docker stats
docker stats

# Check logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

**Free Tier Limits:**
- RAM: 6GB (monitor if you hit it)
- Disk: 200GB total (plenty for portfolio)
- CPU: 1 OCPU (watch for slowness)

### Step 26: View Logs

```bash
# Recent logs
docker-compose -f docker-compose.prod.yml logs --tail=50

# Live logs
docker-compose -f docker-compose.prod.yml logs -f

# Just backend
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Step 27: SSL Renewal (Auto)

```bash
# Create renewal script
cat > ~/renew-ssl.sh << 'EOF'
#!/bin/bash
sudo certbot renew --quiet
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /home/ubuntu/Portfolio/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /home/ubuntu/Portfolio/nginx/ssl/key.pem
docker-compose -f /home/ubuntu/Portfolio/docker-compose.prod.yml restart nginx
EOF

chmod +x ~/renew-ssl.sh

# Schedule renewal (once per month is fine, cert is good for 90 days)
crontab -e
# Add line: 0 3 1 * * /home/ubuntu/renew-ssl.sh
```

---

## Free Tier Limitations & Solutions

### ⚠️ If Services Slow Down

Free tier has 1 OCPU - if everything runs slow:

```bash
# Check CPU usage
docker stats

# You might see high CPU usage on first build
# Solution: This is normal on first build, it gets faster

# If persistently slow, check memory
free -h

# If memory is full, restart
docker-compose -f docker-compose.prod.yml restart
```

### ⚠️ If Disk Fills Up

```bash
# Check disk usage
df -h

# If > 90% used:
# 1. Check what's using space
du -sh ~/Portfolio/*

# 2. Clean old backups if you created any
rm -rf ~/Portfolio/backups/*.db

# 3. Clean Docker
docker system prune -a
```

### ⚠️ If You Exceed Free Tier

You'll get an email from Oracle. To avoid charges:

```bash
# Continue monitoring with free tier only:
# - 1 instance only (6GB RAM, 1 OCPU)
# - 10GB object storage
# - No paid services

# If you hit limits, delete extra resources
docker-compose -f docker-compose.prod.yml down
# Keep it simple, stay under free tier
```

---

## 🎯 Essential Commands Reference

**Connect to Instance:**
```bash
ssh -i ~/key.pem opc@YOUR_IP
```

**Check Service Status:**
```bash
docker-compose -f docker-compose.prod.yml ps
```

**View Logs:**
```bash
docker-compose -f docker-compose.prod.yml logs -f backend
```

**Restart Services:**
```bash
docker-compose -f docker-compose.prod.yml restart
```

**Stop Services:**
```bash
docker-compose -f docker-compose.prod.yml down
```

**Free Disk Space:**
```bash
docker system prune -a
```

**Check Resources:**
```bash
docker stats
free -h
df -h
```

---

## ✅ You're Live!

Your portfolio is now at: **`https://yourdomain.com`**

**What's Running:**
- ✅ Frontend React app
- ✅ Backend FastAPI server
- ✅ Nginx reverse proxy
- ✅ SSL/TLS encryption
- ✅ Rate limiting & security
- ✅ All on FREE tier

**Costs:**
- Domain: $0.99 first year
- Oracle Cloud: $0 (free tier)
- SSL Certificate: $0 (Let's Encrypt)
- **Total Year 1**: ~$12
- **Year 2+**: ~$12/year (domain only)

---

## 🚨 If Something Breaks

1. **Check logs first:**
   ```bash
   docker-compose -f docker-compose.prod.yml logs
   ```

2. **Restart everything:**
   ```bash
   docker-compose -f docker-compose.prod.yml down
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **SSH into instance:**
   ```bash
   ssh -i ~/key.pem ubuntu@YOUR_IP
   ```

4. **Check resources:**
   ```bash
   docker stats
   df -h
   free -h
   ```

5. **Check Docker:**
   ```bash
   docker ps -a
   docker logs CONTAINER_NAME
   ```

---

## 📚 Support Docs

- **SECURITY.md** - How security works
- **DEPLOYMENT_SECURITY.md** - Advanced deployment
- **DEPLOYMENT_CHECKLIST.md** - Pre-deployment verification

---

**Status**: 🟢 **LIVE ON FREE TIER**  
**Date**: April 8, 2026  
**Estimated Monthly Cost**: $0 (free tier)
