from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Tag, Project, BlogPost, TeamMember, Roadmap, Event
from .serializers import TagSerializer, ProjectSerializer, BlogPostSerializer, TeamMemberSerializer, RoadmapSerializer, EventSerializer

# Global search view
@api_view(['GET'])
def global_search(request):
    """
    Global search across all content types.
    Query parameter: ?q=search_term

    Returns:
    {
        "query": "search term",
        "blogs": [...],
        "projects": [...],
        "team": [...],
        "events": [...],
        "roadmaps": [...],
        "tags": [...]
    }
    """
    query = request.query_params.get('q', '').strip()

    if not query or len(query) < 2:
        return Response({
            "query": query,
            "error": "Search query must be at least 2 characters",
            "blogs": [],
            "projects": [],
            "team": [],
            "events": [],
            "roadmaps": [],
            "tags": []
        })

    # Search BlogPosts by title, summary, content, author_name
    blogs = BlogPost.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query) |
        Q(content__icontains=query) |
        Q(author_name__icontains=query)
    ).order_by('-published_date')[:10]

    # Search Projects by title, description, content, author_name
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(content__icontains=query) |
        Q(author_name__icontains=query)
    ).order_by('-published_date')[:10]

    # Search Team Members by name, role, bio, skills
    team = TeamMember.objects.filter(
        Q(name__icontains=query) |
        Q(role__icontains=query) |
        Q(bio__icontains=query) |
        Q(skills__icontains=query)
    ).order_by('position_rank')[:10]

    # Search Events by title, summary, content, author_name
    events = Event.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query) |
        Q(content__icontains=query) |
        Q(author_name__icontains=query)
    ).order_by('-event_date')[:10]

    # Search Roadmaps by title, description, content
    roadmaps = Roadmap.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(content__icontains=query)
    ).order_by('-published_date')[:10]

    # Search Tags by name
    tags = Tag.objects.filter(
        Q(name__icontains=query)
    )[:10]

    return Response({
        "query": query,
        "blogs": BlogPostSerializer(blogs, many=True).data,
        "projects": ProjectSerializer(projects, many=True).data,
        "team": TeamMemberSerializer(team, many=True).data,
        "events": EventSerializer(events, many=True).data,
        "roadmaps": RoadmapSerializer(roadmaps, many=True).data,
        "tags": TagSerializer(tags, many=True).data
    })

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