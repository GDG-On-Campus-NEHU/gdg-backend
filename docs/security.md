# Security Baseline

## Purpose

Summarize current security controls and recommended hardening actions.

## Current controls

- Django auth + session/basic auth in DRF
- Staff-gated writes via custom permission on mutable endpoints
- CSRF trusted origins configured
- CORS origin list configured (with optional override)
- `SECURE_PROXY_SSL_HEADER` set for reverse-proxy TLS

## Hardening recommendations

1. **Set `DJANGO_DEBUG=False` in production**
2. **Replace `ALLOWED_HOSTS=['*']` with explicit hostnames**
3. Keep `CORS_ALLOW_ALL_ORIGINS=false` for production
4. Rotate `DJANGO_SECRET_KEY` using secret manager
5. Restrict admin access by network/IP if platform allows
6. Enforce HTTPS end-to-end

## Secrets handling

- Do not commit `.env`
- Store all sensitive values in deployment secret manager
- Keep `.env.example` non-sensitive and template-only

## Access control model

- Public read endpoints are expected for website consumption
- Content modifications require authenticated staff accounts
- Use least-privilege admin account management
