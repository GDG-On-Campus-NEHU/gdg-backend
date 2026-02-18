# Architecture

## Purpose

Explain how the backend is structured and how data flows from requests to persistent storage.

## High-level components

- **Django project**: `backend_core`
- **Primary app**: `landing_page`
- **HTTP API**: Django REST Framework viewsets + custom API views
- **Admin CMS**: Django admin for content management
- **Database**: SQLite locally, PostgreSQL in production through `DATABASE_URL`
- **Caching**: Django LocMem cache with response-level soft/hard TTL strategy

## Request flow

1. Client calls `/api/...`
2. Router dispatches to `landing_page.urls`
3. Viewset/function builds payload (or fetches from cache)
4. Serializer converts model instances to JSON
5. Response returned via DRF `Response`

## API groups

- CRUD-ish resources: `/api/blog/`, `/api/projects/`, `/api/roadmaps/`, `/api/events/`
- Read-only resources: `/api/team/`, `/api/tags-admin/`
- Aggregate/public utility endpoints:
  - `/api/bootstrap/`
  - `/api/tags/`
  - `/api/tags/popular/`
  - `/api/tags/<slug>/`
  - `/api/items/`
  - `/api/search/`

## Permissions model

- Global DRF default: `IsAuthenticatedOrReadOnly`
- Resource viewsets for blog/projects/roadmaps/events enforce `IsAdminUserOrReadOnly`
- Team and tags admin endpoints are read-only viewsets

## Caching design

The API cache wraps payload generation in `cached_payload()`.

- **Key includes**: request path + cache generation + code version
- **Soft TTL**: stale content can be served while background refresh runs
- **Hard TTL**: blocking refresh after expiry
- **Invalidation**: model `post_save` / `post_delete` signals invalidate hot keys and bump generation

## Content model intent

- Rich content: blog/project/event/roadmap `content`
- Images: externally hosted URL fields (`image_url`, `photo_url`)
- Tags: reusable taxonomy shared across most content types
- Events: extended metadata (mode, registration, speakers, resources, gallery images)

## Non-functional choices

- Static files served with WhiteNoise
- CORS enabled for frontend origins
- `ALLOWED_HOSTS=['*']` currently permissive (see security doc for recommendations)
