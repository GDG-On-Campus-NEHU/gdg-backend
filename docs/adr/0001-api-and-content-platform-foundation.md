# ADR 0001: API and Content Platform Foundation

- Status: Accepted
- Date: 2026-02-18

## Context

The project needs a maintainable backend for website content (blogs, projects, events, roadmaps, team) with public read access and controlled write operations.

## Decision

- Use Django + Django REST Framework for API and admin CMS.
- Use externally hosted media URLs instead of local media uploads for most content assets.
- Use tag taxonomy for cross-content discovery and filtering.
- Add response-level caching with configurable TTL and generation-based invalidation.

## Alternatives considered

1. Fully custom CMS frontend + bespoke APIs
   - Rejected due to timeline and maintenance overhead.
2. Storing media files directly in app disk
   - Rejected for deployment/storage simplicity concerns.
3. No response cache
   - Rejected for read-heavy endpoint performance risk.

## Consequences

- Fast operational setup through Django admin and DRF viewsets.
- Reduced media storage burden on backend.
- Additional complexity in cache invalidation and freshness management.
