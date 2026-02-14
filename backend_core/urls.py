from django.contrib import admin
from django.urls import include, path

# Main URL configuration for Google Developer's Group, NEHU backend
# All landing page API endpoints are under /api/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('landing_page.urls')),
]

urlpatterns += [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Note: Media files (images) are now hosted externally (e.g., Imgur, Cloudinary)
# to save server storage costs on free-tier deployments
