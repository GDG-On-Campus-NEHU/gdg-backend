from django.contrib import admin
from django.urls import include, path

from .views import ping


# Main URL configuration for Google Developer's Group, NEHU backend
# All landing page API endpoints are under /api/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('landing_page.urls')),
    path('ping/', ping),
]

urlpatterns += [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]
