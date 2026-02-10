from django.db import models
from django.utils import timezone

try:
    from ckeditor.fields import RichTextField
except ImportError:  # fallback for environments without CKEditor
    RichTextField = models.TextField


# Model for reusable tags (e.g., "Robotics", "AI/ML")
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Model for the Project Showcase section
class Project(models.Model):
    # Short title shown in lists and cards
    title = models.CharField(max_length=100)
    # Short description used in cards and previews
    description = models.TextField()
    # Rich text content for the detail page
    content = RichTextField(blank=True)
    # Optional featured image
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
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
    content = RichTextField(blank=True)
    # Optional featured image
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
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
    # Profile photo
    photo = models.ImageField(upload_to='team_photos/')
    # Short bio shown on profile/detail view
    bio = models.TextField(blank=True, help_text="Short bio about the team member")
    # Comma-separated skills list (converted to array in serializer)
    skills = models.TextField(blank=True, help_text="Comma-separated skills (e.g., 'Python, Django, React')")
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
    content = RichTextField(blank=True)
    # Optional author attribution
    author_name = models.CharField(max_length=100, blank=True)
    # Publish timestamp used for ordering
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# New model for Events
class Event(models.Model):
    # Event title
    title = models.CharField(max_length=150)
    # Short summary for list cards
    summary = models.TextField()
    # Rich text content for details page
    content = RichTextField(blank=True)
    # Optional event image
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    # Optional organizer or author
    author_name = models.CharField(max_length=100, blank=True)
    # Event date/time
    event_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
