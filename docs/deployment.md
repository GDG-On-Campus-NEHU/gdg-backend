# Deployment

## Purpose

Describe how this service is built, configured, and released.

## Runtime model

- WSGI app served by Gunicorn.
- `Procfile` command:
  - `web: gunicorn backend_core.wsgi:application --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 120`

## Build pipeline

`build.sh` performs:

1. `pip install -r requirements.txt`
2. `python manage.py collectstatic --no-input`
3. `python manage.py migrate`

## Required environment variables

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (set `False` in production)
- `DATABASE_URL` (PostgreSQL recommended)

## Optional env vars (recommended)

- `API_RESPONSE_CACHE_ENABLED` (`true|false`)
- `API_CACHE_CODE_VERSION` (bump to force cache namespace refresh)
- `API_CACHE_SOFT_TTL_SECONDS`
- `API_CACHE_HARD_TTL_SECONDS`
- `API_CACHE_LOCK_TIMEOUT_SECONDS`
- `CORS_ALLOW_ALL_ORIGINS` (`false` in production)

## Platform/network expectations

- App listens on port `8080`.
- Service should expose `/ping/` as health endpoint.
- Ensure frontend origin(s) are present in both CORS and CSRF settings.

## Release checklist

1. Merge reviewed PR into main.
2. Deploy build using current `build.sh`.
3. Run smoke checks:
   - `GET /ping/`
   - `GET /api/bootstrap/`
   - `GET /api/events/`
4. Optionally warm cache:
   - `python manage.py refresh_cache`

## Rollback strategy

- Redeploy previous successful artifact/commit.
- If rollback includes schema changes, verify backward-compatible migrations before rollback.
- Disable API response cache (`API_RESPONSE_CACHE_ENABLED=false`) temporarily if stale behavior is suspected.
