import hashlib
import threading

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import close_old_connections
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response

from .models import (
    BOOTSTRAP_CACHE_DIRTY_KEY,
    CACHE_TIMEOUT_SECONDS,
    EVENTS_LIST_CACHE_KEY,
    BlogPost,
    Event,
    Project,
    Roadmap,
    Tag,
    TeamMember,
)
from .serializers import (
    BasicTagSerializer,
    BlogPostSerializer,
    EventSerializer,
    ProjectSerializer,
    RoadmapSerializer,
    TagSerializer,
    TeamMemberSerializer,
)

VALID_TYPES = {'blogs', 'projects', 'events', 'roadmaps', 'team', 'all'}
CACHE_TTL_SECONDS = CACHE_TIMEOUT_SECONDS
BOOTSTRAP_CACHE_KEY = 'landing:bootstrap:v1'
API_CACHE_GENERATION_KEY = 'api:cache:generation'
API_CACHE_CODE_VERSION = getattr(settings, 'API_CACHE_CODE_VERSION', 'v1')
API_CACHE_ENABLED = getattr(settings, 'API_RESPONSE_CACHE_ENABLED', True)
API_CACHE_SOFT_TTL_SECONDS = getattr(settings, 'API_CACHE_SOFT_TTL_SECONDS', 5 * 60)
API_CACHE_HARD_TTL_SECONDS = getattr(settings, 'API_CACHE_HARD_TTL_SECONDS', 60 * 60)
API_CACHE_LOCK_TIMEOUT_SECONDS = getattr(settings, 'API_CACHE_LOCK_TIMEOUT_SECONDS', 60)


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

    payload = {
        'id': obj.id,
        'type': item_type,
        'title': getattr(obj, 'title', None) or getattr(obj, 'name', ''),
        'summary': summary or '',
        'image_url': image_url or '',
        'tags': BasicTagSerializer(obj.tags.all(), many=True).data,
    }

    if item_type == 'team':
        payload['role'] = getattr(obj, 'role', '')
    if item_type == 'roadmaps':
        icon_name = getattr(obj, 'icon_name', '')
        payload['icon_name'] = icon_name
        payload['emoji'] = icon_name

    return payload


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


def _cache_enabled():
    return API_CACHE_ENABLED


def _cache_generation():
    generation = cache.get(API_CACHE_GENERATION_KEY)
    if generation is None:
        generation = '0'
        cache.set(API_CACHE_GENERATION_KEY, generation, timeout=None)
    return str(generation)


def bump_api_cache_generation():
    cache.set(API_CACHE_GENERATION_KEY, str(timezone.now().timestamp()), timeout=None)


def _cache_base_key(request, namespace):
    raw_key = f"{namespace}|{request.get_full_path()}|{_cache_generation()}|{API_CACHE_CODE_VERSION}"
    key_hash = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()
    return f"api-cache:{key_hash}"


def _store_cached_payload(base_key, payload):
    now_ts = timezone.now().timestamp()
    meta = {
        'soft_expires_at_ts': now_ts + API_CACHE_SOFT_TTL_SECONDS,
        'hard_expires_at_ts': now_ts + API_CACHE_HARD_TTL_SECONDS,
        'generated_at_ts': now_ts,
    }
    cache.set(f'{base_key}:payload', payload, API_CACHE_HARD_TTL_SECONDS)
    cache.set(f'{base_key}:meta', meta, API_CACHE_HARD_TTL_SECONDS)


def _refresh_payload(base_key, builder):
    payload = builder()
    _store_cached_payload(base_key, payload)
    return payload


def _refresh_payload_in_background(base_key, builder):
    lock_key = f'{base_key}:lock'
    if not cache.add(lock_key, True, API_CACHE_LOCK_TIMEOUT_SECONDS):
        return

    def _runner():
        try:
            close_old_connections()
            _refresh_payload(base_key, builder)
        finally:
            cache.delete(lock_key)
            close_old_connections()

    threading.Thread(target=_runner, daemon=True).start()


def cached_payload(request, namespace, builder):
    if not _cache_enabled():
        return builder()

    base_key = _cache_base_key(request, namespace)
    payload_key = f'{base_key}:payload'
    meta_key = f'{base_key}:meta'
    lock_key = f'{base_key}:lock'

    payload = cache.get(payload_key)
    meta = cache.get(meta_key) or {}
    now_ts = timezone.now().timestamp()

    if payload is None:
        if cache.add(lock_key, True, API_CACHE_LOCK_TIMEOUT_SECONDS):
            try:
                return _refresh_payload(base_key, builder)
            finally:
                cache.delete(lock_key)
        return builder()

    if now_ts >= meta.get('hard_expires_at_ts', 0):
        if cache.add(lock_key, True, API_CACHE_LOCK_TIMEOUT_SECONDS):
            try:
                return _refresh_payload(base_key, builder)
            finally:
                cache.delete(lock_key)
        return payload

    if now_ts >= meta.get('soft_expires_at_ts', 0):
        _refresh_payload_in_background(base_key, builder)

    return payload


def _build_bootstrap_payload():
    tags = list(Tag.objects.all().order_by('name'))
    tag_counts = _get_tag_counts('all')
    for tag in tags:
        setattr(tag, 'count', tag_counts.get(tag.id, 0))

    tags_popular_payload = sorted(tags, key=lambda tag: tag.count, reverse=True)[:10]

    events = list(
        Event.objects.all()
        .order_by('-event_date')
        .prefetch_related('tags', 'speakers', 'tech_tag_items', 'gallery_image_items', 'resource_items')[:8]
    )

    items_by_type = {}
    for item_type in ('blogs', 'projects', 'events', 'roadmaps', 'team'):
        queryset = _build_items_queryset(item_type=item_type, sort='recent')[:8]
        items_by_type[item_type] = [_serialize_item(obj, item_type) for obj in queryset]

    return {
        'meta': {
            'generated_at': timezone.now().isoformat(),
            'source': 'cache',
        },
        'tags': TagSerializer(tags, many=True).data,
        'tags_popular': TagSerializer(tags_popular_payload, many=True).data,
        'events': EventSerializer(events, many=True).data,
        'items_by_type': items_by_type,
    }


def refresh_bootstrap_cache(force=False):
    if force or _cache_enabled():
        from django.test.client import RequestFactory

        request = RequestFactory().get('/api/bootstrap/')
        return cached_payload(request, 'bootstrap', _build_bootstrap_payload)
    return _build_bootstrap_payload()


@api_view(['GET'])
def landing_bootstrap(request):
    payload = cached_payload(request, 'bootstrap', _build_bootstrap_payload)
    return Response(payload)


@api_view(['GET'])
def tags_list(request):
    include_counts = _parse_bool(request.query_params.get('include_counts'), default=False)
    item_type = _parse_type(request.query_params.get('type'))

    def _build_payload():
        tags = list(Tag.objects.all().order_by('name'))
        counts = _get_tag_counts(item_type) if include_counts else {}

        for tag in tags:
            setattr(tag, 'count', counts.get(tag.id, 0))

        return {'tags': TagSerializer(tags, many=True).data}

    payload = cached_payload(request, 'tags-list', _build_payload)
    return Response(payload)


@api_view(['GET'])
def tag_detail(request, slug):
    def _build_payload():
        tag = _find_tag_by_slug(slug)
        if not tag:
            return {'detail': 'Not found.'}, 404

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

        return {
            'tag': TagSerializer(tag).data,
            'items': items,
            'pagination': {
                'page': current_page.number,
                'per_page': per_page,
                'total': paginator.count,
            },
        }, 200

    payload, status_code = cached_payload(request, f'tag-detail:{slug}', _build_payload)
    return Response(payload, status=status_code)


@api_view(['GET'])
def items_list(request):
    item_type = _parse_type(request.query_params.get('type'))
    tag_value = request.query_params.get('tag')
    q = request.query_params.get('q', '').strip()
    page = _parse_int(request.query_params.get('page', 1), default=1)
    per_page = _parse_int(request.query_params.get('per_page', 20), default=20, max_value=100)
    sort = request.query_params.get('sort', 'recent').lower()

    def _build_payload():
        tag = _resolve_tag(tag_value)
        if tag_value and not tag:
            return {'items': [], 'pagination': {'page': page, 'per_page': per_page, 'total': 0}}

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

        return {
            'items': list(current_page.object_list),
            'pagination': {
                'page': current_page.number,
                'per_page': per_page,
                'total': paginator.count,
            },
        }

    payload = cached_payload(request, 'items-list', _build_payload)
    return Response(payload)


@api_view(['GET'])
def tags_popular(request):
    limit = _parse_int(request.query_params.get('limit', 10), default=10, max_value=50)

    def _build_payload():
        counts = _get_tag_counts('all')
        tags = list(Tag.objects.filter(id__in=counts.keys()))
        for tag in tags:
            setattr(tag, 'count', counts.get(tag.id, 0))

        tags.sort(key=lambda x: x.count, reverse=True)
        return {'tags': TagSerializer(tags[:limit], many=True).data}

    payload = cached_payload(request, 'tags-popular', _build_payload)
    return Response(payload)


@api_view(['GET'])
def global_search(request):
    query = request.query_params.get('q', '').strip()

    def _build_payload():
        if not query or len(query) < 2:
            return {
                'query': query,
                'error': 'Search query must be at least 2 characters',
                'blogs': [],
                'projects': [],
                'team': [],
                'events': [],
                'roadmaps': [],
                'tags': [],
            }

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

        return {
            'query': query,
            'blogs': BlogPostSerializer(blogs, many=True).data,
            'projects': ProjectSerializer(projects, many=True).data,
            'team': TeamMemberSerializer(team, many=True).data,
            'events': EventSerializer(events, many=True).data,
            'roadmaps': RoadmapSerializer(roadmaps, many=True).data,
            'tags': TagSerializer(tags, many=True).data,
        }

    payload = cached_payload(request, 'global-search', _build_payload)
    return Response(payload)


class CachedReadRetrieveMixin:
    def _cache_namespace(self, action):
        return f'viewset:{self.__class__.__name__}:{action}'

    def list(self, request, *args, **kwargs):
        parent_list = super(CachedReadRetrieveMixin, self).list
        payload = cached_payload(
            request,
            self._cache_namespace('list'),
            lambda: parent_list(request, *args, **kwargs).data,
        )
        return Response(payload)

    def retrieve(self, request, *args, **kwargs):
        parent_retrieve = super(CachedReadRetrieveMixin, self).retrieve
        payload = cached_payload(
            request,
            self._cache_namespace('retrieve'),
            lambda: parent_retrieve(request, *args, **kwargs).data,
        )
        return Response(payload)


class ProjectViewSet(CachedReadRetrieveMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-published_date')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class BlogPostViewSet(CachedReadRetrieveMixin, viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-published_date')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TeamMemberViewSet(CachedReadRetrieveMixin, viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.all().order_by('position_rank')
    serializer_class = TeamMemberSerializer


class RoadmapViewSet(CachedReadRetrieveMixin, viewsets.ModelViewSet):
    queryset = Roadmap.objects.all().order_by('-published_date')
    serializer_class = RoadmapSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class EventViewSet(CachedReadRetrieveMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-event_date').prefetch_related(
        'tags', 'speakers', 'tech_tag_items', 'gallery_image_items', 'resource_items'
    )
    serializer_class = EventSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TagViewSet(CachedReadRetrieveMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
