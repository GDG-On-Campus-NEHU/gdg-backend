import re

from django.core.management.base import BaseCommand
from django.db import transaction

from landing_page.models import BlogPost, Event, Project, Roadmap

YOUTUBE_RE = re.compile(r'https?://(?:www\.)?youtube\.com/watch\?v=([\w-]+)')
YOUTU_BE_RE = re.compile(r'https?://youtu\.be/([\w-]+)')


def normalize_html(value: str) -> str:
    if not value:
        return value

    normalized = value
    normalized = normalized.replace('text-align:left', 'text-align: left')
    normalized = normalized.replace('text-align:center', 'text-align: center')
    normalized = normalized.replace('text-align:right', 'text-align: right')

    normalized = re.sub(
        r'<iframe[^>]*src="https?://(?:www\.)?youtube\.com/embed/([\w-]+)[^>]*></iframe>',
        lambda m: f'<oembed url="https://www.youtube.com/watch?v={m.group(1)}"></oembed>',
        normalized,
        flags=re.IGNORECASE,
    )

    normalized = YOUTUBE_RE.sub(lambda m: f'https://www.youtube.com/watch?v={m.group(1)}', normalized)
    normalized = YOUTU_BE_RE.sub(lambda m: f'https://www.youtube.com/watch?v={m.group(1)}', normalized)

    class_map = {
        'image_left': 'image-style-align-left',
        'image_right': 'image-style-align-right',
        'image_center': 'image-style-align-center',
    }
    for source, target in class_map.items():
        normalized = normalized.replace(source, target)

    return normalized


class Command(BaseCommand):
    help = 'Normalize legacy CKEditor 4 HTML for CKEditor 5 rendering compatibility.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show intended changes without saving them.')
        parser.add_argument('--apply', action='store_true', help='Persist normalized HTML to the database.')

    @transaction.atomic
    def handle(self, *args, **options):
        apply = options['apply']
        dry_run = options['dry_run'] or not apply

        models = [Project, BlogPost, Roadmap, Event]
        updated = 0

        for model in models:
            for obj in model.objects.all().only('id', 'content'):
                original = obj.content or ''
                normalized = normalize_html(original)
                if original == normalized:
                    continue

                updated += 1
                self.stdout.write(f'{model.__name__}#{obj.id} needs normalization')

                if apply:
                    obj.content = normalized
                    obj.save(update_fields=['content'])

        if dry_run:
            self.stdout.write(self.style.WARNING(f'DRY RUN complete. {updated} record(s) would be updated.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Applied normalization to {updated} record(s).'))
