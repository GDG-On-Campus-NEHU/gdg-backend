# GDG NEHU Backend API

Django REST backend for the GDG NEHU website. It powers content for blogs, projects, events, roadmaps, tags, and team members.

## Tech stack

- Python 3.11+
- Django 5
- Django REST Framework
- django-ckeditor-5
- SQLite (default for local), PostgreSQL via `DATABASE_URL` in production
- WhiteNoise for static assets

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API root: `http://127.0.0.1:8000/api/`  
Admin: `http://127.0.0.1:8000/admin/`  
Health check: `http://127.0.0.1:8000/ping/`

## Documentation map

- Project docs index: [`docs/README.md`](docs/README.md)
- Architecture: [`docs/architecture.md`](docs/architecture.md)
- Local setup: [`docs/setup-local.md`](docs/setup-local.md)
- Deployment and environments: [`docs/deployment.md`](docs/deployment.md)
- API reference: [`docs/api.md`](docs/api.md)
- Database and models: [`docs/database.md`](docs/database.md)
- Runbook: [`docs/runbook.md`](docs/runbook.md)
- Testing: [`docs/testing.md`](docs/testing.md)
- Monitoring and reliability checks: [`docs/monitoring.md`](docs/monitoring.md)
- Security baseline: [`docs/security.md`](docs/security.md)
- Architecture decisions: [`docs/adr/`](docs/adr)
- Contribution workflow: [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Operational highlights

- Write operations on blog/projects/roadmaps/events are staff-only; read is public.
- Team and tags-admin endpoints are read-only.
- API responses are cached with soft/hard TTL controls.
- Cache can be warmed with `python manage.py refresh_cache`.
- Rich-text legacy cleanup command: `python manage.py normalize_richtext_html --dry-run`.

## License / ownership

Maintained by GDG NEHU tech team.
