# Database and Schema

## Purpose

Document the primary data model and migration expectations.

## Database configuration

- Database backend is resolved from `DATABASE_URL`.
- Default local DB: SQLite (`db.sqlite3`).
- PostgreSQL options are automatically set when PostgreSQL engine is detected.

## Core models

- `Tag`: reusable taxonomy (`name`, `slug`, `color`)
- `BlogPost`: title/summary/content/image_url/author/tags/published_date
- `Project`: title/description/content/image_url/author/tags/published_date
- `Roadmap`: icon_name/title/description/content/author/tags/published_date
- `TeamMember`: profile + skills + socials + sortable `position_rank`
- `Speaker`: event speaker profile
- `Event`: content + schedule + mode + registration + location/meeting links + relations
- `EventTechTag`: event-specific technology labels
- `EventGalleryImage`: event gallery URLs
- `EventResource`: event resource links

## Relationship notes

- Most content entities have many-to-many relationship with `Tag`.
- `Event` has many-to-many relationship with `Speaker`.
- `Event` has one-to-many children for tech tags, gallery images, resources.

## Migrations

- All migrations live under `landing_page/migrations/`.
- Apply migrations with `python manage.py migrate`.
- Create migrations with `python manage.py makemigrations`.

## Data integrity and defaults

- Tag slug is generated on save if missing.
- Publish/event dates default to `timezone.now`.
- Team display order uses ascending `position_rank`.

## Content normalization command

- `python manage.py normalize_richtext_html --dry-run`
- `python manage.py normalize_richtext_html --apply`

This migrates legacy rich-text HTML patterns for CKEditor 5 compatibility.
