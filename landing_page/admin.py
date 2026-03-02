from django.contrib import admin
from django import forms

try:
    from django_ckeditor_5.widgets import CKEditor5Widget
except ImportError:  # fallback for environments without CKEditor 5
    CKEditor5Widget = forms.Textarea



def rich_text_widget():
    try:
        return CKEditor5Widget(config_name='default')
    except TypeError:
        return CKEditor5Widget()

from .models import (
    Tag,
    Project,
    ProjectContributor,
    BlogPost,
    TeamMember,
    Roadmap,
    Event,
    Speaker,
    EventTechTag,
    EventGalleryImage,
    EventResource,
)


# Register your models here so they appear in the admin panel.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProjectAdminForm(forms.ModelForm):
    content = forms.CharField(widget=rich_text_widget(), required=False)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectContributorInline(admin.StackedInline):
    model = ProjectContributor
    extra = 1
    fields = (
        'name',
        'role_type',
        'photo_url',
        'github_url',
        'linkedin_url',
        'website_url',
        'order',
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'author_name', 'status', 'is_open_source', 'published_date')
    search_fields = ('title', 'description', 'author_name', 'contributors__name')
    list_filter = ('published_date', 'tags', 'is_open_source', 'status')
    inlines = (ProjectContributorInline,)
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'description', 'content', 'image_url')}),
        ('Meta', {'fields': ('author_name', 'published_date', 'tags')}),
        ('Links & Status', {'fields': ('is_open_source', 'status', 'repo_url', 'demo_url')}),
    )


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=rich_text_widget(), required=False)

    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'author_name', 'published_date')
    search_fields = ('title', 'summary', 'author_name')
    list_filter = ('published_date', 'tags')


class RoadmapAdminForm(forms.ModelForm):
    content = forms.CharField(widget=rich_text_widget(), required=False)

    class Meta:
        model = Roadmap
        fields = '__all__'


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    form = RoadmapAdminForm
    list_display = ('title', 'author_name', 'published_date')
    search_fields = ('title', 'description', 'author_name')
    list_filter = ('published_date', 'tags')


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'social_link')
    search_fields = ('name', 'bio', 'social_link')


class EventAdminForm(forms.ModelForm):
    content = forms.CharField(widget=rich_text_widget(), required=False)

    class Meta:
        model = Event
        fields = '__all__'


class TechTagInline(admin.TabularInline):
    model = EventTechTag
    extra = 1


class GalleryImageInline(admin.TabularInline):
    model = EventGalleryImage
    extra = 1


class ResourceInline(admin.TabularInline):
    model = EventResource
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'author_name', 'event_date', 'registration_deadline', 'mode', 'requires_registration')
    search_fields = ('title', 'summary', 'author_name', 'location_address', 'meeting_link', 'registration_link')
    list_filter = ('event_date', 'registration_deadline', 'mode', 'requires_registration', 'tags')
    filter_horizontal = ('tags', 'speakers')
    fieldsets = (
        (None, {'fields': ('title', 'summary', 'content', 'image_url', 'author_name')}),
        ('Schedule & Access', {'fields': ('event_date', 'registration_deadline', 'requires_registration', 'registration_link')}),
        ('Venue', {'fields': ('mode', 'location_address', 'meeting_link')}),
        ('Relations', {'fields': ('tags', 'speakers')}),
    )
    inlines = (TechTagInline, GalleryImageInline, ResourceInline)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'position_rank')
    search_fields = ('name', 'role', 'bio', 'skills')
    list_filter = ('position_rank', 'tags')
