from django.contrib import admin
from django import forms

try:
    from ckeditor.widgets import CKEditorWidget
except ImportError:  # fallback for environments without CKEditor
    CKEditorWidget = forms.Textarea

from .models import Tag, Project, BlogPost, TeamMember, Roadmap, Event

# Register your models here so they appear in the admin panel.
admin.site.register(Tag)

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
    list_filter = ('published_date',)

class EventAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Event
        fields = '__all__'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'author_name', 'event_date')
    search_fields = ('title', 'summary', 'author_name')
    list_filter = ('event_date',)

admin.site.register(TeamMember)
