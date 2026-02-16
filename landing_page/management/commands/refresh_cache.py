from django.core.management.base import BaseCommand

from landing_page.models import warm_tag_event_cache


class Command(BaseCommand):
    help = 'Warms the in-memory cache for Tag and Event GET payloads.'

    def handle(self, *args, **options):
        warm_tag_event_cache()
        self.stdout.write(self.style.SUCCESS('In-memory cache refreshed for Tag and Event data.'))
