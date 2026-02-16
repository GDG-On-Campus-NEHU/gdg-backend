from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

try:
    from django_ckeditor_5.fields import CKEditor5Field
except ImportError:  # fallback for environments without CKEditor
    CKEditor5Field = models.TextField


# Model for reusable tags (e.g., "Robotics", "AI/ML")
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True, null=True)
    color = models.CharField(max_length=7, default="#7da6ff")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or 'tag'
            candidate = base_slug
            suffix = 1
            while Tag.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Model for the Project Showcase section
class Project(models.Model):
    # Short title shown in lists and cards
    title = models.CharField(max_length=100)
    # Short description used in cards and previews
    description = models.TextField()
    # Rich text content for the detail page
    content = CKEditor5Field('Text', config_name='default', blank=True)
    # External image URL (e.g., Imgur, Cloudinary) - saves server storage
    image_url = models.URLField(blank=True, max_length=500, help_text="URL to externally hosted image (e.g., Imgur)")
    # Optional tags for filtering
    tags = models.ManyToManyField(Tag, blank=True)
    # Optional author attribution
    author_name = models.CharField(max_length=100, blank=True)
    # Publish timestamp used for ordering
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# Model for the Latest Blogs section
class BlogPost(models.Model):
    # Title shown in lists and page header
    title = models.CharField(max_length=200)
    # Short summary used in preview cards
    summary = models.TextField(help_text="A short summary for the landing page card.")
    # Rich text content for the detail page
    content = CKEditor5Field('Text', config_name='default', blank=True)
    # External image URL (e.g., Imgur, Cloudinary) - saves server storage
    image_url = models.URLField(blank=True, max_length=500, help_text="URL to externally hosted image (e.g., Imgur)")
    # Optional tags for filtering
    tags = models.ManyToManyField(Tag, blank=True)
    # Optional author attribution
    author_name = models.CharField(max_length=100, blank=True)
    # Publish timestamp used for ordering
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# Model for the Our Team section
class TeamMember(models.Model):
    # Display name
    name = models.CharField(max_length=100)
    # Role/title for the team section
    role = models.CharField(max_length=100)
    # External photo URL (e.g., Imgur, Cloudinary) - saves server storage
    photo_url = models.URLField(max_length=500, blank=True, default='', help_text="URL to externally hosted photo (e.g., Imgur)")
    # Short bio shown on profile/detail view
    bio = models.TextField(blank=True, help_text="Short bio about the team member")
    # Comma-separated skills list (converted to array in serializer)
    skills = models.TextField(blank=True, help_text="Comma-separated skills (e.g., 'Python, Django, React')")
    # Optional tags for filtering/search pages
    tags = models.ManyToManyField(Tag, blank=True)
    # Sorting rank for display order
    position_rank = models.PositiveIntegerField(default=99,
                                                help_text="Lower number = higher seniority (e.g., 1 for President)")
    # Social links
    github_url = models.URLField(blank=True, max_length=200)
    linkedin_url = models.URLField(blank=True, max_length=200)
    instagram_url = models.URLField(blank=True, max_length=200)
    twitter_url = models.URLField(blank=True, max_length=200)
    website_url = models.URLField(blank=True, max_length=200)

    def __str__(self):
        return self.name

# Model for the Roadmaps section
class Roadmap(models.Model):
    # Icon/emoji shown with the roadmap title
    icon_name = models.CharField(max_length=50, help_text="e.g., '🤖' or 'circuit-board'")
    # Roadmap title
    title = models.CharField(max_length=100)
    # Short description shown in cards
    description = models.TextField()
    # Rich text content for the detail page
    content = CKEditor5Field('Text', config_name='default', blank=True)
    # Optional tags for filtering
    tags = models.ManyToManyField(Tag, blank=True)
    # Optional author attribution
    author_name = models.CharField(max_length=100, blank=True)
    # Publish timestamp used for ordering
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Speaker(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.URLField(max_length=500, help_text="URL to externally hosted speaker photo")
    bio = models.TextField()
    social_link = models.URLField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.name


# New model for Events
class Event(models.Model):
    MODE_PHYSICAL = 'physical'
    MODE_VIRTUAL = 'virtual'
    MODE_HYBRID = 'hybrid'
    MODE_CHOICES = [
        (MODE_PHYSICAL, 'Physical'),
        (MODE_VIRTUAL, 'Virtual'),
        (MODE_HYBRID, 'Hybrid'),
    ]

    # Event title
    title = models.CharField(max_length=150)
    # Short summary for list cards
    summary = models.TextField()
    # Rich text content for details page
    content = CKEditor5Field('Text', config_name='default', blank=True)
    # External image URL (e.g., Imgur, Cloudinary) - saves server storage
    image_url = models.URLField(blank=True, max_length=500, help_text="URL to externally hosted image (e.g., Imgur)")
    # Optional tags for filtering
    tags = models.ManyToManyField(Tag, blank=True)
    # Optional organizer or author
    author_name = models.CharField(max_length=100, blank=True)
    # Event date/time
    event_date = models.DateTimeField(default=timezone.now)
    speakers = models.ManyToManyField(Speaker, blank=True, related_name='events')
    requires_registration = models.BooleanField(default=True)
    registration_link = models.URLField(blank=True, null=True, max_length=500)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default=MODE_PHYSICAL)
    location_address = models.CharField(max_length=255, blank=True)
    meeting_link = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return self.title


class EventTechTag(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tech_tag_items')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EventGalleryImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gallery_image_items')
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return self.image_url


class EventResource(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='resource_items')
    label = models.CharField(max_length=100)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.label


CACHE_TIMEOUT_SECONDS = 60 * 60
TAG_CACHE_KEY = 'tags:list:False:all'
EVENTS_LIST_CACHE_KEY = 'events:list'


def warm_tag_event_cache():
    from .serializers import EventSerializer, TagSerializer

    tags = list(Tag.objects.all().order_by('name'))
    events = list(
        Event.objects.all()
        .order_by('-event_date')
        .prefetch_related('tags', 'speakers', 'tech_tag_items', 'gallery_image_items', 'resource_items')
    )

    cache.set(TAG_CACHE_KEY, {'tags': TagSerializer(tags, many=True).data}, CACHE_TIMEOUT_SECONDS)
    cache.set(EVENTS_LIST_CACHE_KEY, EventSerializer(events, many=True).data, CACHE_TIMEOUT_SECONDS)

    for event in events:
        cache.set(f'events:detail:{event.id}', EventSerializer(event).data, CACHE_TIMEOUT_SECONDS)


@receiver(post_save, sender=Tag)
@receiver(post_delete, sender=Tag)
@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def refresh_tag_event_cache_on_change(**kwargs):
    warm_tag_event_cache()
