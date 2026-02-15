from django.contrib import admin
from django.urls import include, path

from .views import ping

admin.site.site_header = 'GDG NEHU Admin'
admin.site.site_title = 'Club Portal'
admin.site.index_title = 'Club Management Dashboard'

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
