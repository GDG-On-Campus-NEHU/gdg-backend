# API Reference

## Purpose

Summarize available endpoints, payload shapes, and permissions.

## Base URL

- Local: `http://127.0.0.1:8000/api/`

## Authentication and permissions

- Read requests are public for API resources.
- Writes for blog/projects/roadmaps/events require a staff-authenticated user.
- Session auth + Basic auth are enabled.

## Core resource endpoints

### Blog posts

- `GET /api/blog/`
- `POST /api/blog/` (staff)
- `GET /api/blog/{id}/`
- `PUT/PATCH /api/blog/{id}/` (staff)
- `DELETE /api/blog/{id}/` (staff)

Response shape:
- `GET /api/blog/` returns summary fields (excludes `content`): `id`, `title`, `summary`, `image_url`, `tags`, `author_name`, `published_date`
- `GET /api/blog/{id}/` returns full detail fields (includes `content`)
- Write payloads still accept `content` and `tag_ids` (staff)

### Projects

- `GET /api/projects/`
- `POST /api/projects/` (staff)
- `GET /api/projects/{id}/`
- `PUT/PATCH /api/projects/{id}/` (staff)
- `DELETE /api/projects/{id}/` (staff)

Response shape:
- `GET /api/projects/` returns summary fields (excludes `content`): `id`, `title`, `description`, `image_url`, `tags`, `author_name`, `published_date`
- `GET /api/projects/{id}/` returns full detail fields (includes `content`)
- Write payloads still accept `content` and `tag_ids` (staff)

### Events

- `GET /api/events/`
- `POST /api/events/` (staff)
- `GET /api/events/{id}/`
- `PUT/PATCH /api/events/{id}/` (staff)
- `DELETE /api/events/{id}/` (staff)

Response shape:
- `GET /api/events/` returns summary fields (excludes `content`)
- `GET /api/events/{id}/` returns full detail fields (includes `content`)

Fields include:
- Core: `id`, `title`, `summary`, `image_url`, `author_name`, `event_date` (+ `content` on detail)
- Registration/mode: `requires_registration`, `registration_link`, `registration_deadline`, `registration_open`, `mode`, `location_address`, `meeting_link`
- Relations: `tags`, `tag_ids` (write), `tech_tags`, `speakers`, `gallery_images`, `resources`

Event validation behavior:
- If `requires_registration=true` and `registration_link` is provided, `registration_deadline` is required.
- When both `registration_deadline` and `event_date` are present, `registration_deadline` must be less than or equal to `event_date`.
- `registration_open` is a computed read-only boolean: true when registration is required and still open by deadline (or when a registration link exists with no deadline).

### Roadmaps

- `GET /api/roadmaps/`
- `POST /api/roadmaps/` (staff)
- `GET /api/roadmaps/{id}/`
- `PUT/PATCH /api/roadmaps/{id}/` (staff)
- `DELETE /api/roadmaps/{id}/` (staff)

Response shape:
- `GET /api/roadmaps/` returns summary fields (excludes `content`): `id`, `icon_name`, `title`, `description`, `tags`, `author_name`, `published_date`
- `GET /api/roadmaps/{id}/` returns full detail fields (includes `content`)
- Write payloads still accept `content` and `tag_ids` (staff)

### Team members (read-only)

- `GET /api/team/`
- `GET /api/team/{id}/`

Response shape:
- `GET /api/team/` returns summary fields (excludes `bio`)
- `GET /api/team/{id}/` returns full detail fields (includes `bio`)

Fields:
- `id`, `name`, `role`, `photo_url`, `skills`, `skills_list`, `tags`, `position_rank`, social URLs (+ `bio` on detail)

### Tags admin listing (read-only)

- `GET /api/tags-admin/`
- `GET /api/tags-admin/{id}/`

## Aggregate/search endpoints

### `GET /api/bootstrap/`
Returns homepage-oriented payload:
- `meta`
- `tags`
- `tags_popular`
- `events`
- `items_by_type`

Notes:
- Aggregate payloads are intentionally lightweight and use summary representations.
- Rich text body fields such as `content` are only available on resource detail endpoints (`/api/{resource}/{id-or-slug}/`).

### `GET /api/tags/`
Query params:
- `include_counts=true|false`
- `type=blogs|projects|events|roadmaps|team|all`

### `GET /api/tags/popular/`
Query params:
- `limit` (max 50)

### `GET /api/tags/{slug}/`
Query params:
- `type`, `page`, `per_page`, `sort`

### `GET /api/items/`
Query params:
- `type`, `tag`, `q`, `page`, `per_page`, `sort`

### `GET /api/search/`
Query params:
- `q` (minimum length: 2)

Returns grouped results for blogs/projects/team/events/roadmaps/tags.

Search results return summary representations (no full rich-text body content).

## Health endpoint

- `GET /ping/` → `pong`
