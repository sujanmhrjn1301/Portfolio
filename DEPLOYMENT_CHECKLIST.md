# 🚀 Pre-Deployment Security Checklist

Before deploying to production, go through this checklist step by step.

## Phase 1: Code Review & Security

- [ ] **No secrets in code**: Search for hardcoded API keys
  ```bash
  grep -r "sk-or-v1-" backend/ frontend/
  grep -r "token=" backend/ frontend/
  grep -r "password=" backend/ frontend/
  ```

- [ ] **Auth implemented**: API key/JWT required for sensitive endpoints
  ```bash
  # Check main.py for @depends(verify_api_key_or_token)
  grep -n "verify_api_key_or_token" backend/main.py
  ```

- [ ] **Input validation**: All user inputs sanitized
  ```bash
  grep -n "validate_" backend/main.py
  ```

- [ ] **Rate limiting**: Configured on all endpoints
  ```bash
  grep -n "rate_limit" backend/main.py
  ```

- [ ] **Error handling**: No stack traces exposed
  ```bash
  grep -n "create_secure_error_response" backend/main.py
  ```

- [ ] **Logging**: Sensitive data not logged
  ```bash
  grep -n "logger.debug" backend/main.py | head -5
  ```

## Phase 2: Dependencies & Versions

- [ ] **Pinned versions**: No floating versions in requirements.txt
  ```bash
  grep "==" backend/requirements.txt
  ```

- [ ] **No vulnerable packages**: Run security check
  ```bash
  pip-audit --requirements backend/requirements.txt
  ```

- [ ] **Updated packages**: Run latest versions
  ```bash
  pip list --outdated
  ```

## Phase 3: Environment Configuration

- [ ] **Environment variables created**: Copy `.env.production.example` to `.env`
  ```bash
  cp .env.production.example .env
  # Edit .env with real prod values
  ```

- [ ] **All required env vars set**:
  ```bash
  required_vars="ENVIRONMENT DEBUG SECRET_KEY API_KEY OPENROUTER_API_KEY CORS_ORIGINS"
  for var in $required_vars; do
    if [ -z "${!var}" ]; then
      echo "❌ Missing: $var"
    else
      echo "✓ $var set"
    fi
  done
  ```

- [ ] **Production values not in git**:
  ```bash
  git status .env
  # Should show: ignored by git
  ```

- [ ] **CORS restricted to your domain**:
  ```bash
  echo $CORS_ORIGINS
  # Should NOT include localhost
  ```

## Phase 4: Docker Images

- [ ] **Backend image runs as non-root**:
  ```bash
  docker build -t portfolio-backend backend/
  docker run --rm portfolio-backend id
  # Should show: uid=1000(appuser)
  ```

- [ ] **Frontend image runs as non-root**:
  ```bash
  docker build -t portfolio-frontend frontend/
  docker run --rm portfolio-frontend id
  # Should show: uid=1000(appuser)
  ```

- [ ] **Health checks configured**: Docker compose file has health checks
  ```bash
  grep -n "healthcheck:" docker-compose.prod.yml
  ```

- [ ] **No secrets in Dockerfile**: No hardcoded API keys
  ```bash
  grep -r "ENV.*KEY\|ENV.*TOKEN" backend/Dockerfile frontend/Dockerfile
  ```

## Phase 5: Nginx Configuration

- [ ] **SSL/TLS certificates installed**:
  ```bash
  ls -la nginx/ssl/
  # Should show: cert.pem, key.pem
  ```

- [ ] **SSL configuration correct**:
  ```bash
  grep -n "ssl_certificate" nginx/nginx.conf
  grep -n "ssl_protocols" nginx/nginx.conf
  ```

- [ ] **Security headers configured**:
  ```bash
  grep -n "add_header" nginx/nginx.conf | wc -l
  # Should show: >= 5 headers
  ```

- [ ] **HTTPS redirect configured**:
  ```bash
  grep -n "return 301 https" nginx/nginx.conf
  ```

- [ ] **Rate limiting configured**:
  ```bash
  grep -n "limit_req_zone\|limit_req " nginx/nginx.conf
  ```

## Phase 6: Database & Backups

- [ ] **Database backup script exists**:
  ```bash
  ls -la backups/
  # Or set up automated backups
  ```

- [ ] **Backup tested**: Restore from backup works
  ```bash
  # Test restore procedure
  docker-compose -f docker-compose.prod.yml down
  # Restore from backup
  docker-compose -f docker-compose.prod.yml up -d
  ```

- [ ] **Backup location secure**: Outside web root, encrypted if possible
  ```bash
  # Backups not accessible via web
  grep -n "backups" nginx/nginx.conf
  ```

## Phase 7: Monitoring & Logging

- [ ] **Logging configured**: Apps log to files/stdout
  ```bash
  grep -n "logging:" docker-compose.prod.yml
  ```

- [ ] **Log rotation configured**: Prevents disk fill
  ```bash
  grep -n "max-size\|max-file" docker-compose.prod.yml
  ```

- [ ] **Monitoring alerts set up**: For errors and rate limits
  ```bash
  # Check monitoring service status
  ```

- [ ] **Access logs enabled**: Audit trail exists
  ```bash
  grep -n "access_log" nginx/nginx.conf
  ```

## Phase 8: Testing & Validation

- [ ] **API tests pass**:
  ```bash
  curl -f http://localhost:8000/health
  curl -f http://localhost:3000/
  ```

- [ ] **CORS test**:
  ```bash
  curl -i -X OPTIONS http://localhost/api/chat \
    -H "Origin: https://example.com"
  # Check Access-Control headers
  ```

- [ ] **Auth test**:
  ```bash
  curl -X POST http://localhost:8000/ingest-cv \
    -H "Authorization: Bearer invalid-token"
  # Should return 401
  ```

- [ ] **Rate limit test**:
  ```bash
  for i in {1..15}; do
    curl http://localhost:8000/health
  done
  # Some should return 429
  ```

- [ ] **SSL test**:
  ```bash
  nmap --script ssl-enum-ciphers -p 443 yourdomain.com
  # Check TLS 1.2+ only
  ```

## Phase 9: Security Scan

- [ ] **OWASP scan**: Run OWASP ZAP or similar
  ```bash
  # Use OWASP ZAP to scan endpoints
  ```

- [ ] **Dependency scan**: Check for known vulnerabilities
  ```bash
  pip-audit
  npm audit
  ```

- [ ] **File permissions**: Correct ownership and permissions
  ```bash
  ls -la backend/ frontend/
  # All files owned by user, not world-writable
  ```

## Phase 10: Documentation

- [ ] **SECURITY.md complete**: All security measures documented
  ```bash
  wc -l SECURITY.md
  ```

- [ ] **DEPLOYMENT_SECURITY.md complete**: Deployment process documented
  ```bash
  wc -l DEPLOYMENT_SECURITY.md
  ```

- [ ] **Incident response plan**: Know what to do if compromised
  ```bash
  grep -i "incident\|compromise" SECURITY.md
  ```

- [ ] **Support contact**: Know who to contact for issues
  ```bash
  grep -i "support\|contact" SECURITY.md
  ```

## Phase 11: Final Checklist

- [ ] **All team members briefed**: Everyone knows security procedures
- [ ] **Backups tested**: Can restore if needed
- [ ] **Monitoring active**: Alerts will notify if problems
- [ ] **Runbooks created**: Team knows what to do
- [ ] **Change log updated**: Document deployment date and changes
- [ ] **Approval**: Project lead approves deployment

## Deployment Steps

```bash
# 1. Load environment
source .env

# 2. Build images
docker-compose -f docker-compose.prod.yml build

# 3. Start services
docker-compose -f docker-compose.prod.yml up -d

# 4. Verify health
sleep 5
docker-compose -f docker-compose.prod.yml ps

# 5. Test endpoints
curl https://yourdomain.com/health
curl https://yourdomain.com/api/health

# 6. Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Post-Deployment

- [ ] **Monitor for errors**: Check logs every 5 minutes for 1 hour
- [ ] **Test functionality**: Go through key user flows
- [ ] **Check metrics**: Monitor CPU, memory, disk
- [ ] **Review security events**: Check for failed auth attempts
- [ ] **Announce deployment**: Notify stakeholders

---

**Status**: Ready for production  
**Last Reviewed**: April 8, 2026  
**Next Review**: October 8, 2026

---

## Questions?

Refer to:
- [SECURITY.md](SECURITY.md) - Security overview
- [DEPLOYMENT_SECURITY.md](DEPLOYMENT_SECURITY.md) - Deployment guide
- [README.md](README.md) - Project overview
