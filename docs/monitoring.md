# Monitoring and Reliability

## Purpose

Define practical health checks and reliability signals for this backend.

## Health endpoints

- `GET /ping/` should return `200 pong`
- `GET /api/bootstrap/` should return `200` with JSON payload

## Key signals to monitor

- Request latency (p95) for:
  - `/api/bootstrap/`
  - `/api/items/`
  - `/api/search/`
- Error rate (4xx/5xx split)
- Database connection failures/timeouts
- Gunicorn worker restarts/timeouts

## Suggested alerts

- `/ping/` failing for 2+ consecutive intervals
- 5xx rate above baseline threshold
- p95 latency above acceptable SLO for 5+ minutes

## Cache behavior checks

- Verify cache toggle (`API_RESPONSE_CACHE_ENABLED`) effect during incidents
- Bump `API_CACHE_CODE_VERSION` during major payload-shape changes
- Run `python manage.py refresh_cache` post-deploy for high-traffic windows

## Logging recommendations

- Capture access logs for status and latency
- Capture application logs for exceptions
- Keep deploy markers in logs for correlation
