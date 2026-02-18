# Operations Runbook

## Purpose

Day-2 operations guide for common incidents and maintenance tasks.

## Routine tasks

### Warm API cache

```bash
python manage.py refresh_cache
```

Use after deploys or content-heavy updates.

### Normalize legacy rich text

```bash
python manage.py normalize_richtext_html --dry-run
python manage.py normalize_richtext_html --apply
```

### Reset or create admin account

```bash
python scripts/create_or_reset_superuser.py
```

Outputs credentials to stdout. Rotate after emergency use.

## Incident playbooks

### API latency spike

1. Check `/ping/` health.
2. Check DB connectivity (`DATABASE_URL` validity).
3. Temporarily disable response cache if stale lock contention is suspected:
   - `API_RESPONSE_CACHE_ENABLED=false`
4. Redeploy and recheck `/api/bootstrap/` and `/api/events/`.

### CORS or CSRF failures

1. Confirm frontend domain appears in:
   - `CORS_ALLOWED_ORIGINS`
   - `CSRF_TRUSTED_ORIGINS`
2. Confirm proxy forwards HTTPS headers correctly (`SECURE_PROXY_SSL_HEADER`).

### Unexpected 401/403 on writes

1. Confirm request is authenticated.
2. Confirm user is `is_staff=True`.
3. Confirm endpoint is one of staff-write resources.

## Smoke checks after deploy

```bash
curl -i http://<host>/ping/
curl -i http://<host>/api/bootstrap/
curl -i http://<host>/api/events/
```

## Rollback checklist

1. Roll back to previous stable release.
2. Re-run smoke checks.
3. If schema-related issue, verify migration compatibility.
4. Rewarm cache if needed.
