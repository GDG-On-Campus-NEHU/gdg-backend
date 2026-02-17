from django.core.management.base import BaseCommand
from django.test import Client

from landing_page.models import (
    BlogPost,
    Event,
    Project,
    Roadmap,
    Tag,
    TeamMember,
    warm_tag_event_cache,
)


class Command(BaseCommand):
    help = 'Warms in-memory cache for bootstrap and all public JSON API endpoints.'

    def _warm_paths(self):
        paths = [
            '/api/bootstrap/',
            '/api/tags/',
            '/api/tags/?include_counts=true&type=all',
            '/api/tags/popular/',
            '/api/items/?type=all&page=1&per_page=20&sort=recent',
            '/api/search/?q=ai',
            '/api/projects/',
            '/api/blog/',
            '/api/team/',
            '/api/roadmaps/',
            '/api/events/',
            '/api/tags-admin/',
        ]

        for tag in Tag.objects.all()[:100]:
            slug = tag.slug
            if slug:
                paths.append(f'/api/tags/{slug}/?type=blogs&page=1&per_page=20&sort=recent')

        for obj in Project.objects.all()[:200]:
            paths.append(f'/api/projects/{obj.id}/')
        for obj in BlogPost.objects.all()[:200]:
            paths.append(f'/api/blog/{obj.id}/')
        for obj in TeamMember.objects.all()[:200]:
            paths.append(f'/api/team/{obj.id}/')
        for obj in Roadmap.objects.all()[:200]:
            paths.append(f'/api/roadmaps/{obj.id}/')
        for obj in Event.objects.all()[:200]:
            paths.append(f'/api/events/{obj.id}/')

        return paths

    def handle(self, *args, **options):
        warm_tag_event_cache()

        client = Client()
        failures = []
        total = 0

        for path in self._warm_paths():
            total += 1
            response = client.get(path)
            if response.status_code >= 400:
                failures.append((path, response.status_code))

        if failures:
            for path, status_code in failures:
                self.stdout.write(self.style.WARNING(f'Warm failed: {path} -> {status_code}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'In-memory cache refresh attempted for {total} endpoint paths; failures={len(failures)}.'
            )
        )
