# 🔐 Security Documentation

**Last Updated**: April 8, 2026  
**Status**: Production-Ready

---

## Table of Contents

1. [Security Overview](#security-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Input Validation](#input-validation)
4. [Rate Limiting](#rate-limiting)
5. [CORS & Headers](#cors--headers)
6. [Error Handling](#error-handling)
7. [Data Protection](#data-protection)
8. [Deployment Security](#deployment-security)
9. [Incident Response](#incident-response)

---

## Security Overview

This portfolio system has been hardened with enterprise-grade security measures:

✅ **Authentication**: JWT-based token system  
✅ **Rate Limiting**: Per-endpoint request throttling  
✅ **Input Validation**: All user inputs sanitized  
✅ **CORS**: Restricted to approved origins  
✅ **Headers**: Security headers on all responses  
✅ **Error Handling**: No information disclosure  
✅ **Logging**: Audit trails for sensitive operations  
✅ **Environment**: Configuration-based secrets management  

---

## Authentication & Authorization

### Public Endpoints (No Auth Required)

These endpoints are open for anyone to use:

- `GET /health` - Health check
- `POST /chat` - Send messages
- `GET /shared/{share_id}` - Access shared conversations
- `POST /conversations` - Create conversations
- `GET /conversations` - List conversations
- `GET /conversations/{id}` - Get conversation history
- `GET /portfolio-info` - Public portfolio info
- `GET /github/repositories` - GitHub projects

### Protected Endpoints (Auth Required)

These endpoints require API key or JWT token:

- `POST /ingest-cv` - Upload CV data
- `DELETE /conversations/{id}` - Delete conversations
- `PATCH /conversations/{id}` - Update conversations

### How to Authenticate

**Option 1: API Key (Recommended for automation)**

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  -X POST http://localhost:8000/ingest-cv \
  -H "Content-Type: application/json" \
  -d '{"cv_text": "..."}'
```

Set `API_KEY` environment variable:

```bash
export API_KEY=your-secure-api-key-here
```

**Option 2: JWT Token (For users)**

Get a token in development:

```bash
curl http://localhost:8000/auth/token
```

Returns:

```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

Use the token:

```bash
curl -H "Authorization: Bearer eyJhbGc..." \
  -X POST http://localhost:8000/ingest-cv
```

**In Production**: Use your authentication service instead of `/auth/token`

---

## Input Validation

### Validated Fields

| Field | Type | Max Length | Rules |
|-------|------|-----------|-------|
| `message` | string | 5,000 chars | Non-empty, no control characters |
| `title` | string | 200 chars | Non-empty or defaults to "New Chat" |
| `conversation_id` | UUID | 36 chars | Valid UUID v4 format |
| `share_id` | UUID | 36 chars | Valid UUID format |
| `cv_text` | string | 1 MB | Non-empty |

### Validation Examples

```python
# Message validation
validate_message_content(user_message)

# Title validation
validate_title(conversation_title)

# ID validation
validate_conversation_id(conv_id)
validate_share_id(share_id)
```

### XSS Prevention

- All inputs sanitized before storage
- Control characters removed
- HTML/script content filtered
- Frontend uses React which auto-escapes by default

---

## Rate Limiting

### Rate Limit Rules

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/chat` | 10 requests | 60 seconds |
| `/* (general)` | 100 requests | 60 seconds |
| `/ingest-cv` | 5 requests | 5 minutes |

### Rate Limit Headers

Responses include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1712617200
```

### When Rate Limited

```http
HTTP/429 Too Many Requests

{
  "error": "Too many requests",
  "message": "Rate limit exceeded. Please try again later.",
  "status_code": 429
}
```

---

## CORS & Headers

### Allowed Origins

**Development** (localhost only):
- http://localhost:3000
- http://127.0.0.1:3000
- http://localhost:8000
- http://127.0.0.1:8000

**Production** (configure in `CORS_ORIGINS` env):
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Allowed Methods

Only specific HTTP methods allowed:
- `GET` - Read data
- `POST` - Create data
- `PUT` - Replace data
- `PATCH` - Partial update
- `DELETE` - Delete data
- `OPTIONS` - CORS pre-flight

### Security Headers (All Responses)

Every response includes:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
```

---

## Error Handling

### Secure Error Responses

Errors never expose stack traces or internal details:

```json
{
  "error": "Internal server error",
  "message": "An error occurred processing your request",
  "status_code": 500
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad request (invalid input)
- `401` - Unauthorized (auth required/failed)
- `403` - Forbidden (permission denied)
- `404` - Not found
- `429` - Rate limited
- `500` - Server error (never leaks details)

### Development Debugging

In development mode (`DEBUG=true`), full error details logged server-side only:

```python
logger.error(f"Error details: {exception}", exc_info=True)
```

**Never** sent to frontend in production.

---

## Data Protection

### Sensitive Information

**NOT exposed via API:**
- Phone numbers
- Physical addresses
- Private emails
- API keys
- Database credentials
- Full stack traces

**Public portfolio info only:**
- Name
- GitHub URL
- LinkedIn URL

### Chat History Protection

- Stored in SQLite (can be encrypted)
- Only accessible to conversation owner
- Shared conversations have unique IDs (not sequential)
- No sensitive data stored by default

### Secret Management

All secrets in environment variables:

```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-xxxx

# Optional
GITHUB_TOKEN=ghp_xxxx
API_KEY=your-api-key
SECRET_KEY=your-secret-key
```

**Never commit `.env` files!**

Files that should NEVER be in git:
- `.env` (real secrets)
- `.env.*.local`
- `*.pyc`
- `__pycache__/`
- `node_modules/`
- `.DS_Store`

---

## Deployment Security

### Pre-Deployment Checklist

```bash
# 1. Verify configuration
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=use-secure-random-value

# 2. Change all secrets
OPENROUTER_API_KEY=your-production-key
GITHUB_TOKEN=your-production-token
API_KEY=strong-random-api-key

# 3. Set production CORS origins
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# 4. Enable HTTPS/TLS
# Use reverse proxy (Nginx) with SSL certificates

# 5. Run security checks
# - No git history includes secrets
# - No debug endpoints exposed
# - Rate limiting enabled
# - HTTPS enforced
```

### Docker Security

```dockerfile
# Don't run as root
USER appuser

# No secrets in Dockerfile
# Secrets via environment only

# Use multi-stage builds (already implemented)

# Pin dependency versions
requirements.txt  # All pinned with ==
```

### HTTPS/TLS

Use a reverse proxy in production:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Redirect HTTP to HTTPS
    if ($scheme != "https") {
        return 301 https://$server_name$request_uri;
    }
    
    location /api {
        proxy_pass http://backend:8000;
    }
}
```

---

## Incident Response

### If You Discover a Vulnerability

1. **Don't** make the issue public on GitHub
2. Email security details to: `security@example.com`
3. Include:
   - Vulnerability description
   - Affected endpoint(s)
   - Steps to reproduce
   - Suggested fix (if available)

### Compromised Secrets

If you accidentally commit secrets:

1. **Immediately revoke**:
   ```bash
   # Rotate all compromised keys
   OPENROUTER_API_KEY=new-key
   GITHUB_TOKEN=new-token
   API_KEY=new-key
   SECRET_KEY=new-key
   ```

2. **Clean git history**:
   ```bash
   git filter-branch --force --index-filter \
     'git rm -r --cached --ignore-unmatch .env' \
     --prune-empty -x HEAD
   git push origin --force --all
   ```

3. **Force new deployment** with new keys

### Security Updates

- Keep dependencies updated (`pip list --outdated`)
- Monitor security advisories
- Test updates before production deployment
- Use automated dependency scanning

---

## Security Audit Checklist

Review before each deployment:

- [ ] All secrets in environment variables (not in code)
- [ ] `SECRET_KEY` changed from default
- [ ] `DEBUG=false` in production
- [ ] CORS origins restricted to your domain
- [ ] HTTPS/TLS certificate valid
- [ ] Rate limiting enabled and configured
- [ ] Authentication required for admin endpoints
- [ ] Error messages don't leak stack traces
- [ ] API keys have proper scope/permissions
- [ ] Logs don't contain sensitive data
- [ ] Database encrypted (if applicable)
- [ ] Backups tested and working
- [ ] Monitoring and alerting configured

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)

---

## Support

For security questions or issues:
- Check this documentation
- Review error logs
- Test in development environment first
- Contact: `security@example.com`

---

**Last Reviewed**: April 8, 2026  
**Next Review**: October 8, 2026
