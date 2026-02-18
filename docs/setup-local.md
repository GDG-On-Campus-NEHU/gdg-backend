# Local Setup

## Purpose

Get the backend running locally for development and testing.

## Prerequisites

- Python 3.11+
- `pip`

## Steps

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Verify startup

- API root: `http://127.0.0.1:8000/api/`
- Ping: `http://127.0.0.1:8000/ping/`
- Admin: `http://127.0.0.1:8000/admin/`

## Useful commands

```bash
python manage.py test
python manage.py refresh_cache
python manage.py normalize_richtext_html --dry-run
python scripts/create_or_reset_superuser.py
```

## Environment variables

Copy from `.env.example` and adjust:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DATABASE_URL`
- `CSRF_TRUSTED_ORIGINS`
- `API_RESPONSE_CACHE_ENABLED`
- `API_CACHE_CODE_VERSION`
- `API_CACHE_SOFT_TTL_SECONDS`
- `API_CACHE_HARD_TTL_SECONDS`
- `API_CACHE_LOCK_TIMEOUT_SECONDS`
- `CORS_ALLOW_ALL_ORIGINS`

## Troubleshooting

- If migrations fail, verify `DATABASE_URL` format.
- If frontend gets CORS errors, check origin in `CORS_ALLOWED_ORIGINS`.
- If auth-restricted writes fail, use a staff/superuser account.
