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
- `GET /api/blog/{slug}/`
- `PUT/PATCH /api/blog/{slug}/` (staff)
- `DELETE /api/blog/{slug}/` (staff)

Response shape:
- `GET /api/blog/` returns summary fields (excludes `content`): `id`, `slug`, `title`, `summary`, `image_url`, `tags`, `author_name`, `published_date`
- `GET /api/blog/{slug}/` returns full detail fields (includes `content`)
- Write payloads still accept `content` and `tag_ids` (staff)

### Projects

- `GET /api/projects/`
- `POST /api/projects/` (staff)
- `GET /api/projects/{slug}/`
- `PUT/PATCH /api/projects/{slug}/` (staff)
- `DELETE /api/projects/{slug}/` (staff)

Response shape:
- `GET /api/projects/` returns summary fields (excludes `content`): `id`, `slug`, `title`, `description`, `image_url`, `tags`, `author_name`, `published_date`
- `GET /api/projects/{slug}/` returns full detail fields (includes `content`)
- Write payloads still accept `content` and `tag_ids` (staff)

### Events

- `GET /api/events/`
- `POST /api/events/` (staff)
- `GET /api/events/{slug}/`
- `PUT/PATCH /api/events/{slug}/` (staff)
- `DELETE /api/events/{slug}/` (staff)

Response shape:
- `GET /api/events/` returns summary fields (excludes `content`)
- `GET /api/events/{slug}/` returns full detail fields (includes `content`)

Fields include:
- Core: `id`, `slug`, `title`, `summary`, `image_url`, `author_name`, `event_date` (+ `content` on detail)
- Registration/mode: `requires_registration`, `registration_link`, `registration_deadline`, `registration_open`, `mode`, `location_address`, `meeting_link`
- Relations: `tags`, `tag_ids` (write), `tech_tags`, `speakers`, `gallery_images`, `resources`

Event validation behavior:
- If `requires_registration=true` and `registration_link` is provided, `registration_deadline` is required.
- When both `registration_deadline` and `event_date` are present, `registration_deadline` must be less than or equal to `event_date`.
- `registration_open` is a computed read-only boolean: true when registration is required and still open by deadline (or when a registration link exists with no deadline).

### Roadmaps

- `GET /api/roadmaps/`
- `POST /api/roadmaps/` (staff)
- `GET /api/roadmaps/{slug}/`
- `PUT/PATCH /api/roadmaps/{slug}/` (staff)
- `DELETE /api/roadmaps/{slug}/` (staff)

Response shape:
- `GET /api/roadmaps/` returns summary fields (excludes `content`): `id`, `slug`, `icon_name`, `title`, `description`, `tags`, `author_name`, `published_date`
- `GET /api/roadmaps/{slug}/` returns full detail fields (includes `content`)
- Write payloads still accept `content` and `tag_ids` (staff)

### Team members (read-only)

- `GET /api/team/`
- `GET /api/team/{slug}/`

Response shape:
- `GET /api/team/` returns summary fields (excludes `bio`)
- `GET /api/team/{slug}/` returns full detail fields (includes `bio`)

Fields:
- `id`, `slug`, `name`, `role`, `photo_url`, `skills`, `skills_list`, `tags`, `position_rank`, social URLs (+ `bio` on detail)

### Tags admin listing (read-only)

- `GET /api/tags-admin/`
- `GET /api/tags-admin/{id}/`


## Slug migration and numeric URL deprecation

- Detail endpoints now resolve by slug (`{slug}`) for blog/projects/events/roadmaps/team.
- Temporary backward compatibility is enabled: numeric IDs still work on these detail endpoints.
- Numeric ID detail URLs are deprecated and will be removed after **2026-09-01**.
- Update clients to use the `slug` returned in list/detail payloads.

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
- Rich text body fields such as `content` are only available on resource detail endpoints (`/api/{resource}/{slug}/`).

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
