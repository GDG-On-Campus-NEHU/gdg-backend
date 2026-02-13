from django.contrib import admin
from django import forms

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

    class Meta:
        model = Event
        fields = '__all__'

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
