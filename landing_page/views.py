from rest_framework import viewsets
from .models import Tag, Project, BlogPost, TeamMember, Roadmap, Event
from .serializers import TagSerializer, ProjectSerializer, BlogPostSerializer, TeamMemberSerializer, RoadmapSerializer, EventSerializer

# Projects are fully writable for content management
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-published_date')
    serializer_class = ProjectSerializer

# Blog posts are fully writable for content management
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-published_date')
    serializer_class = BlogPostSerializer

# Team members are read-only via API (managed in admin)
class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all().order_by('position_rank')
    serializer_class = TeamMemberSerializer

# Roadmaps are fully writable for content management
class RoadmapViewSet(viewsets.ModelViewSet):
    queryset = Roadmap.objects.all().order_by('-published_date')
    serializer_class = RoadmapSerializer

# Events are fully writable for content management
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-event_date')
    serializer_class = EventSerializer

# Tags are read-only via API (managed in admin)
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer