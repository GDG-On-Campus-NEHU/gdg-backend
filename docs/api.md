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

Fields:
- `id`, `title`, `summary`, `content`, `image_url`, `tags`, `tag_ids` (write), `author_name`, `published_date`

### Projects

- `GET /api/projects/`
- `POST /api/projects/` (staff)
- `GET /api/projects/{id}/`
- `PUT/PATCH /api/projects/{id}/` (staff)
- `DELETE /api/projects/{id}/` (staff)

Fields:
- `id`, `title`, `description`, `content`, `image_url`, `tags`, `tag_ids` (write), `author_name`, `published_date`

### Events

- `GET /api/events/`
- `POST /api/events/` (staff)
- `GET /api/events/{id}/`
- `PUT/PATCH /api/events/{id}/` (staff)
- `DELETE /api/events/{id}/` (staff)

Fields include:
- Core: `id`, `title`, `summary`, `content`, `image_url`, `author_name`, `event_date`
- Registration/mode: `requires_registration`, `registration_link`, `mode`, `location_address`, `meeting_link`
- Relations: `tags`, `tag_ids` (write), `tech_tags`, `speakers`, `gallery_images`, `resources`

### Roadmaps

- `GET /api/roadmaps/`
- `POST /api/roadmaps/` (staff)
- `GET /api/roadmaps/{id}/`
- `PUT/PATCH /api/roadmaps/{id}/` (staff)
- `DELETE /api/roadmaps/{id}/` (staff)

Fields:
- `id`, `icon_name`, `title`, `description`, `content`, `tags`, `tag_ids` (write), `author_name`, `published_date`

### Team members (read-only)

- `GET /api/team/`
- `GET /api/team/{id}/`

Fields:
- `id`, `name`, `role`, `photo_url`, `bio`, `skills`, `skills_list`, `tags`, `tag_ids`, `position_rank`, social URLs

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

## Health endpoint

- `GET /ping/` → `pong`
