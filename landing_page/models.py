from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

try:
    from django_ckeditor_5.fields import CKEditor5Field
except ImportError:  # fallback for environments without CKEditor
    CKEditor5Field = models.TextField

PROJECT_STATUS_IDEA = 'idea'
PROJECT_STATUS_IN_PROGRESS = 'in_progress'
PROJECT_STATUS_COMPLETED = 'completed'
PROJECT_STATUS_ARCHIVED = 'archived'
PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_IDEA, 'Idea'),
    (PROJECT_STATUS_IN_PROGRESS, 'In Progress'),
    (PROJECT_STATUS_COMPLETED, 'Completed'),
    (PROJECT_STATUS_ARCHIVED, 'Archived'),
]


def _generate_unique_slug(model_cls, source_value, instance_pk=None, default_prefix='item', extra_filters=None):
    base_slug = slugify(source_value) or default_prefix
    candidate = base_slug
    suffix = 1
    queryset = model_cls.objects.all()
    if instance_pk:
        queryset = queryset.exclude(pk=instance_pk)
    if extra_filters:
        queryset = queryset.filter(**extra_filters)
    while queryset.filter(slug=candidate).exists():
        candidate = f"{base_slug}-{suffix}"
        suffix += 1
    return candidate


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
    is_open_source = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default=PROJECT_STATUS_IDEA)
    repo_url = models.URLField(blank=True, max_length=500)
    demo_url = models.URLField(blank=True, max_length=500)
    # Optional tags for filtering
    tags = models.ManyToManyField(Tag, blank=True)
    # Optional author attribution
    author_name = models.CharField(max_length=100, blank=True)
    # Publish timestamp used for ordering
    published_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(Project, self.title, instance_pk=self.pk, default_prefix='project')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectContributor(models.Model):
    project = models.ForeignKey(Project, related_name='contributors', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    role_type = models.CharField(max_length=120, blank=True)
    photo_url = models.URLField(blank=True, max_length=500)
    github_url = models.URLField(blank=True, max_length=500)
    linkedin_url = models.URLField(blank=True, max_length=500)
    website_url = models.URLField(blank=True, max_length=500)
    order = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return f"{self.name} – {self.project.title}"

# Model for the Latest Blogs section
class BlogAuthor(models.Model):
    name = models.CharField(max_length=100)
    photo_url = models.URLField(blank=True, max_length=500)
    bio = models.TextField(blank=True)
    github_url = models.URLField(blank=True, max_length=500)
    linkedin_url = models.URLField(blank=True, max_length=500)
    instagram_url = models.URLField(blank=True, max_length=500)
    website_url = models.URLField(blank=True, max_length=500)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


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
    authors = models.ManyToManyField(BlogAuthor, blank=True, related_name='blog_posts')
    # Publish timestamp used for ordering
    published_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(BlogPost, self.title, instance_pk=self.pk, default_prefix='blog')
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(TeamMember, self.name, instance_pk=self.pk, default_prefix='member')
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(Roadmap, self.title, instance_pk=self.pk, default_prefix='roadmap')
        super().save(*args, **kwargs)

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
    registration_deadline = models.DateTimeField(blank=True, null=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default=MODE_PHYSICAL)
    location_address = models.CharField(max_length=255, blank=True)
    meeting_link = models.URLField(blank=True, max_length=500)
    slug = models.SlugField(max_length=170, unique=True, blank=True, null=True)

    def clean(self):
        super().clean()

        if self.requires_registration and self.registration_link and not self.registration_deadline:
            raise ValidationError({
                'registration_deadline': 'Registration deadline is required when registration is enabled and a registration link is provided.'
            })

        if self.registration_deadline and self.event_date and self.registration_deadline > self.event_date:
            raise ValidationError({
                'registration_deadline': 'Registration deadline must be on or before the event date.'
            })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _generate_unique_slug(Event, self.title, instance_pk=self.pk, default_prefix='event')
        self.full_clean()
        super().save(*args, **kwargs)

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
BOOTSTRAP_CACHE_DIRTY_KEY = 'landing:bootstrap:v1:dirty'
API_CACHE_GENERATION_KEY = 'api:cache:generation'


def warm_tag_event_cache():
    from .serializers import (
        BlogPostDetailSerializer,
        BlogPostListSerializer,
        EventDetailSerializer,
        EventListSerializer,
        ProjectDetailSerializer,
        ProjectListSerializer,
        RoadmapDetailSerializer,
        RoadmapListSerializer,
        TagSerializer,
        TeamMemberListSerializer,
    )

    tags = list(Tag.objects.all().order_by('name'))
    cache.set(TAG_CACHE_KEY, {'tags': TagSerializer(tags, many=True).data}, CACHE_TIMEOUT_SECONDS)

    events = list(
        Event.objects.all()
        .order_by('-event_date')
        .prefetch_related('tags', 'speakers', 'tech_tag_items', 'gallery_image_items', 'resource_items')[:5]
    )
    cache.set(EVENTS_LIST_CACHE_KEY, EventListSerializer(events, many=True).data, CACHE_TIMEOUT_SECONDS)
    for event in events:
        cache.set(f'events:detail:{event.id}', EventDetailSerializer(event).data, CACHE_TIMEOUT_SECONDS)

    blogs = list(BlogPost.objects.all().order_by('-published_date').prefetch_related('tags', 'authors')[:5])
    cache.set('blogs:list', BlogPostListSerializer(blogs, many=True).data, CACHE_TIMEOUT_SECONDS)
    for blog in blogs:
        cache.set(f'blogs:detail:{blog.id}', BlogPostDetailSerializer(blog).data, CACHE_TIMEOUT_SECONDS)
        if blog.slug:
            cache.set(f'blogs:detail:slug:{blog.slug}', BlogPostDetailSerializer(blog).data, CACHE_TIMEOUT_SECONDS)

    projects = list(Project.objects.all().order_by('-published_date').prefetch_related('tags', 'contributors')[:5])
    cache.set('projects:list', ProjectListSerializer(projects, many=True).data, CACHE_TIMEOUT_SECONDS)
    for project in projects:
        cache.set(f'projects:detail:{project.id}', ProjectDetailSerializer(project).data, CACHE_TIMEOUT_SECONDS)

    roadmaps = list(Roadmap.objects.all().order_by('-published_date').prefetch_related('tags')[:5])
    cache.set('roadmaps:list', RoadmapListSerializer(roadmaps, many=True).data, CACHE_TIMEOUT_SECONDS)
    for roadmap in roadmaps:
        cache.set(f'roadmaps:detail:{roadmap.id}', RoadmapDetailSerializer(roadmap).data, CACHE_TIMEOUT_SECONDS)

    team_members = list(TeamMember.objects.all().order_by('position_rank').prefetch_related('tags'))
    cache.set('team:list', TeamMemberListSerializer(team_members, many=True).data, CACHE_TIMEOUT_SECONDS)


@receiver(post_save, sender=Tag)
@receiver(post_delete, sender=Tag)
@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
@receiver(post_save, sender=BlogPost)
@receiver(post_delete, sender=BlogPost)
@receiver(post_save, sender=Project)
@receiver(post_delete, sender=Project)
@receiver(post_save, sender=Roadmap)
@receiver(post_delete, sender=Roadmap)
@receiver(post_save, sender=TeamMember)
@receiver(post_delete, sender=TeamMember)
@receiver(post_save, sender=ProjectContributor)
@receiver(post_delete, sender=ProjectContributor)
@receiver(post_save, sender=BlogAuthor)
@receiver(post_delete, sender=BlogAuthor)
def refresh_tag_event_cache_on_change(**kwargs):
    # Phase 2: avoid expensive synchronous cache rebuilds on writes.
    # Invalidate hot keys cheaply and let reads/cron repopulate.
    cache.delete(TAG_CACHE_KEY)
    cache.delete(EVENTS_LIST_CACHE_KEY)
    cache.set(BOOTSTRAP_CACHE_DIRTY_KEY, True, CACHE_TIMEOUT_SECONDS * 6)
    cache.set(API_CACHE_GENERATION_KEY, str(timezone.now().timestamp()), timeout=None)
