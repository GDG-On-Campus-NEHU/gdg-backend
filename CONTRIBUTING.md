# Contributing Guide

## Purpose

Provide a predictable workflow for changes to the GDG NEHU backend.

## Prerequisites

- Python 3.11+
- Virtual environment activated
- Dependencies installed from `requirements.txt`

## Development workflow

1. Create a branch from `main`.
2. Make focused changes with clear commit messages.
3. Run checks before opening PR:
   - `python manage.py test`
   - `python -m compileall .`
4. Update docs when API/model/ops behavior changes.
5. Open PR with:
   - Problem statement
   - What changed
   - Risk and rollback notes

## Coding notes

- Use Django/DRF patterns already present in the repo.
- Preserve staff-write/read-only permission model for public endpoints.
- Prefer additive schema migrations; avoid destructive changes unless necessary.
- Keep cache behavior consistent (bump generation on data-changing operations).

## Documentation expectations

Any change touching one of these areas must update matching docs:

- Endpoint contract changes → `docs/api.md`
- Model/schema changes → `docs/database.md`
- Deployment/env changes → `docs/deployment.md`
- Operational changes → `docs/runbook.md`

## Owner

GDG NEHU backend maintainers.
