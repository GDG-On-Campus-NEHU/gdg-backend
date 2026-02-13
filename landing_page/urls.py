from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TagViewSet,
    ProjectViewSet,
    BlogPostViewSet,
    TeamMemberViewSet,
    RoadmapViewSet,
    EventViewSet,
    global_search,
    tags_list,
    tag_detail,
    items_list,
    tags_popular,
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'blog', BlogPostViewSet)
router.register(r'team', TeamMemberViewSet)
router.register(r'roadmaps', RoadmapViewSet)
router.register(r'events', EventViewSet)
router.register(r'tags-admin', TagViewSet)

urlpatterns = [
    path('tags/', tags_list, name='tags-list'),
    path('tags/popular/', tags_popular, name='tags-popular'),
    path('tags/<slug:slug>/', tag_detail, name='tag-detail'),
    path('items/', items_list, name='items-list'),
    path('search/', global_search, name='global-search'),
    path('', include(router.urls)),
]
