# Testing Strategy

## Purpose

Describe the current automated and manual verification flow.

## Automated tests

Primary test suite:

```bash
python manage.py test
```

Current tests cover:
- Auth rules for write endpoints
- CRUD create behavior for major resources
- Tag count and item aggregation endpoints
- Rich-text normalization logic

## Lightweight static checks

```bash
python -m compileall .
```

Useful to catch syntax/import errors quickly.

## Manual checks

After running server:

- Visit `/ping/`
- Visit `/api/bootstrap/`
- Verify representative endpoints:
  - `/api/blog/`
  - `/api/projects/`
  - `/api/events/`
  - `/api/tags/?include_counts=true&type=all`

Optional scripts:

- `python test_api_endpoints.py`
- `python test_image_upload.py`

## CI recommendation

If CI is introduced/updated, enforce at minimum:

1. `pip install -r requirements.txt`
2. `python manage.py test`
3. `python -m compileall .`
4. markdown link/lint checks for docs
