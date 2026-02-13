from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

try:
    from ckeditor.widgets import CKEditorWidget
except ImportError:  # fallback for environments without CKEditor
    CKEditorWidget = forms.Textarea

from .models import Tag, Project, BlogPost, TeamMember, Roadmap, Event, Speaker

# Register your models here so they appear in the admin panel.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProjectAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Project
        fields = '__all__'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'author_name', 'published_date')
    search_fields = ('title', 'description', 'author_name')
    list_filter = ('published_date', 'tags')

class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=False)

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
    content = forms.CharField(widget=CKEditorWidget(), required=False)

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
    content = forms.CharField(widget=CKEditorWidget(), required=False)
    tech_tags = forms.CharField(
        required=False,
        help_text='Enter tech tags separated by commas (e.g., React, Firebase, Python).',
    )
    gallery_images = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Enter one image URL per line.',
    )
    resources = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Enter one resource per line in "Label | URL" format.',
    )

    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tech_tags'].initial = ', '.join(self.instance.tech_tags or [])
            self.fields['gallery_images'].initial = '\n'.join(self.instance.gallery_images or [])
            resource_lines = []
            for resource in self.instance.resources or []:
                if isinstance(resource, dict):
                    label = (resource.get('label') or '').strip()
                    url = (resource.get('url') or '').strip()
                    if label or url:
                        resource_lines.append(f"{label} | {url}" if label and url else label or url)
            self.fields['resources'].initial = '\n'.join(resource_lines)

    def clean_tech_tags(self):
        value = self.cleaned_data.get('tech_tags', '')
        return [tag.strip() for tag in value.split(',') if tag.strip()]

    def clean_gallery_images(self):
        value = self.cleaned_data.get('gallery_images', '')
        return [url.strip() for url in value.splitlines() if url.strip()]

    def clean_resources(self):
        value = self.cleaned_data.get('resources', '')
        resources = []
        errors = []

        for index, line in enumerate(value.splitlines(), start=1):
            entry = line.strip()
            if not entry:
                continue
            if '|' not in entry:
                errors.append(f'Line {index}: expected "Label | URL" format.')
                continue

            label, url = [part.strip() for part in entry.split('|', 1)]
            if not label or not url:
                errors.append(f'Line {index}: both label and URL are required.')
                continue

            resources.append({'label': label, 'url': url})

        if errors:
            raise ValidationError(errors)

        return resources

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'author_name', 'event_date', 'mode', 'requires_registration')
    search_fields = ('title', 'summary', 'author_name', 'location_address', 'meeting_link', 'registration_link')
    list_filter = ('event_date', 'mode', 'requires_registration', 'tags')
    filter_horizontal = ('tags', 'speakers')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'position_rank')
    search_fields = ('name', 'role', 'bio', 'skills')
    list_filter = ('position_rank', 'tags')
