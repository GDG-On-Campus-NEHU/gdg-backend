from django.core.cache import cache
from django.db.models import Q, Count
from django.utils.text import slugify
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response

from .models import Tag, Project, BlogPost, TeamMember, Roadmap, Event
from .serializers import (
    TagSerializer,
    BasicTagSerializer,
    ProjectSerializer,
    BlogPostSerializer,
    TeamMemberSerializer,
    RoadmapSerializer,
    EventSerializer,
)

VALID_TYPES = {'blogs', 'projects', 'events', 'roadmaps', 'team', 'all'}
CACHE_TTL_SECONDS = 120


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


def _parse_bool(value, default=False):
    if value is None:
        return default
    return str(value).lower() in {'1', 'true', 'yes'}


def _parse_type(value):
    item_type = (value or 'all').lower()
    return item_type if item_type in VALID_TYPES else 'all'


def _count_from_through(model):
    rows = model.tags.through.objects.values('tag_id').annotate(total=Count('id'))
    return {row['tag_id']: row['total'] for row in rows}


def _get_tag_counts(item_type='all'):
    count_maps = {
        'blogs': _count_from_through(BlogPost),
        'projects': _count_from_through(Project),
        'events': _count_from_through(Event),
        'roadmaps': _count_from_through(Roadmap),
        'team': _count_from_through(TeamMember),
    }
    if item_type == 'all':
        combined = {}
        for mapping in count_maps.values():
            for tag_id, count in mapping.items():
                combined[tag_id] = combined.get(tag_id, 0) + count
        return combined
    return count_maps[item_type]


def _parse_int(value, default, min_value=1, max_value=None):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    parsed = max(parsed, min_value)
    if max_value is not None:
        parsed = min(parsed, max_value)
    return parsed


def _find_tag_by_slug(slug):
    direct = Tag.objects.filter(slug=slug).first()
    if direct:
        return direct
    for tag in Tag.objects.all():
        if slugify(tag.name) == slug:
            return tag
    return None


def _resolve_tag(tag_value):
    if not tag_value:
        return None
    if str(tag_value).isdigit():
        return Tag.objects.filter(id=int(tag_value)).first()
    by_slug = Tag.objects.filter(slug=tag_value).first()
    if by_slug:
        return by_slug
    return _find_tag_by_slug(tag_value)


def _serialize_item(obj, item_type):
    if item_type == 'blogs':
        summary = obj.summary
        image_url = obj.image_url
    elif item_type == 'projects':
        summary = obj.description
        image_url = obj.image_url
    elif item_type == 'events':
        summary = obj.summary
        image_url = obj.image_url
    elif item_type == 'roadmaps':
        summary = obj.description
        image_url = ''
    else:
        summary = obj.bio
        image_url = obj.photo_url

    return {
        'id': obj.id,
        'type': item_type,
        'title': getattr(obj, 'title', None) or getattr(obj, 'name', ''),
        'summary': summary or '',
        'image_url': image_url or '',
        'tags': BasicTagSerializer(obj.tags.all(), many=True).data,
    }


def _get_base_queryset(item_type):
    if item_type == 'blogs':
        return BlogPost.objects.prefetch_related('tags').all(), 'published_date'
    if item_type == 'projects':
        return Project.objects.prefetch_related('tags').all(), 'published_date'
    if item_type == 'events':
        return Event.objects.prefetch_related('tags').all(), 'event_date'
    if item_type == 'roadmaps':
        return Roadmap.objects.prefetch_related('tags').all(), 'published_date'
    return TeamMember.objects.prefetch_related('tags').all(), 'position_rank'


def _build_items_queryset(item_type, tag=None, q='', sort='recent'):
    queryset, order_field = _get_base_queryset(item_type)

    if tag is not None:
        queryset = queryset.filter(tags=tag)

    if q:
        if item_type == 'blogs':
            queryset = queryset.filter(Q(title__icontains=q) | Q(summary__icontains=q))
        elif item_type == 'projects':
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        elif item_type == 'events':
            queryset = queryset.filter(Q(title__icontains=q) | Q(summary__icontains=q))
        elif item_type == 'roadmaps':
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        else:
            queryset = queryset.filter(Q(name__icontains=q) | Q(bio__icontains=q))

    if sort == 'popular':
        queryset = queryset.annotate(tag_usage=Count('tags')).order_by('-tag_usage', f'-{order_field}')
    else:
        if item_type == 'team':
            queryset = queryset.order_by(order_field)
        else:
            queryset = queryset.order_by(f'-{order_field}')

    return queryset


@api_view(['GET'])
def tags_list(request):
    include_counts = _parse_bool(request.query_params.get('include_counts'), default=False)
    item_type = _parse_type(request.query_params.get('type'))

    cache_key = f"tags:list:{include_counts}:{item_type}"
    cached = cache.get(cache_key)
    if cached is not None:
        return Response(cached)

    tags = list(Tag.objects.all().order_by('name'))
    counts = _get_tag_counts(item_type) if include_counts else {}

    for tag in tags:
        setattr(tag, 'count', counts.get(tag.id, 0))

    payload = {'tags': TagSerializer(tags, many=True).data}
    cache.set(cache_key, payload, CACHE_TTL_SECONDS)
    return Response(payload)


@api_view(['GET'])
def tag_detail(request, slug):
    tag = _find_tag_by_slug(slug)
    if not tag:
        return Response({'detail': 'Not found.'}, status=404)
    item_type = _parse_type(request.query_params.get('type'))
    page = _parse_int(request.query_params.get('page', 1), default=1)
    per_page = _parse_int(request.query_params.get('per_page', 20), default=20, max_value=100)
    sort = request.query_params.get('sort', 'recent').lower()

    if item_type == 'all':
        item_type = 'blogs'

    counts = _get_tag_counts(item_type)
    setattr(tag, 'count', counts.get(tag.id, 0))

    queryset = _build_items_queryset(item_type=item_type, tag=tag, sort=sort)
    paginator = Paginator(queryset, per_page)
    current_page = paginator.get_page(page)

    items = [_serialize_item(obj, item_type) for obj in current_page.object_list]

    return Response({
        'tag': TagSerializer(tag).data,
        'items': items,
        'pagination': {
            'page': current_page.number,
            'per_page': per_page,
            'total': paginator.count,
        },
    })


@api_view(['GET'])
def items_list(request):
    item_type = _parse_type(request.query_params.get('type'))
    tag_value = request.query_params.get('tag')
    q = request.query_params.get('q', '').strip()
    page = _parse_int(request.query_params.get('page', 1), default=1)
    per_page = _parse_int(request.query_params.get('per_page', 20), default=20, max_value=100)
    sort = request.query_params.get('sort', 'recent').lower()

    tag = _resolve_tag(tag_value)
    if tag_value and not tag:
        return Response({'items': [], 'pagination': {'page': page, 'per_page': per_page, 'total': 0}})

    types_to_query = ['blogs', 'projects', 'events', 'roadmaps', 'team'] if item_type == 'all' else [item_type]

    all_items = []
    for current_type in types_to_query:
        queryset = _build_items_queryset(current_type, tag=tag, q=q, sort=sort)
        for obj in queryset:
            all_items.append((obj, current_type))

    if sort == 'recent':
        def _sort_key(item_tuple):
            obj, current_type = item_tuple
            if current_type == 'events':
                return (0, obj.event_date.timestamp())
            if current_type == 'team':
                return (1, -getattr(obj, 'position_rank', 9999))
            published = getattr(obj, 'published_date', None)
            return (0, published.timestamp() if published else 0)

        if item_type == 'all':
            all_items.sort(key=_sort_key, reverse=True)

    serialized = [_serialize_item(obj, current_type) for obj, current_type in all_items]
    paginator = Paginator(serialized, per_page)
    current_page = paginator.get_page(page)

    return Response({
        'items': list(current_page.object_list),
        'pagination': {
            'page': current_page.number,
            'per_page': per_page,
            'total': paginator.count,
        },
    })


@api_view(['GET'])
def tags_popular(request):
    limit = _parse_int(request.query_params.get('limit', 10), default=10, max_value=50)
    counts = _get_tag_counts('all')

    tags = list(Tag.objects.filter(id__in=counts.keys()))
    for tag in tags:
        setattr(tag, 'count', counts.get(tag.id, 0))

    tags.sort(key=lambda x: x.count, reverse=True)

    return Response({'tags': TagSerializer(tags[:limit], many=True).data})


@api_view(['GET'])
def global_search(request):
    query = request.query_params.get('q', '').strip()

    if not query or len(query) < 2:
        return Response({
            'query': query,
            'error': 'Search query must be at least 2 characters',
            'blogs': [],
            'projects': [],
            'team': [],
            'events': [],
            'roadmaps': [],
            'tags': []
        })

    blogs = BlogPost.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query) |
        Q(content__icontains=query) |
        Q(author_name__icontains=query)
    ).order_by('-published_date')[:10]

    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(content__icontains=query) |
        Q(author_name__icontains=query)
    ).order_by('-published_date')[:10]

    team = TeamMember.objects.filter(
        Q(name__icontains=query) |
        Q(role__icontains=query) |
        Q(bio__icontains=query) |
        Q(skills__icontains=query)
    ).order_by('position_rank')[:10]

    events = Event.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query) |
        Q(content__icontains=query) |
        Q(author_name__icontains=query)
    ).order_by('-event_date')[:10]

    roadmaps = Roadmap.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(content__icontains=query)
    ).order_by('-published_date')[:10]

    tags = Tag.objects.filter(Q(name__icontains=query))[:10]

    return Response({
        'query': query,
        'blogs': BlogPostSerializer(blogs, many=True).data,
        'projects': ProjectSerializer(projects, many=True).data,
        'team': TeamMemberSerializer(team, many=True).data,
        'events': EventSerializer(events, many=True).data,
        'roadmaps': RoadmapSerializer(roadmaps, many=True).data,
        'tags': TagSerializer(tags, many=True).data,
    })


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-published_date')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-published_date')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all().order_by('position_rank')
    serializer_class = TeamMemberSerializer


class RoadmapViewSet(viewsets.ModelViewSet):
    queryset = Roadmap.objects.all().order_by('-published_date')
    serializer_class = RoadmapSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-event_date')
    serializer_class = EventSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
