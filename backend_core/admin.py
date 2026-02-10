from django.contrib import admin
from django.conf import settings

# Use a generic club name in admin site headers
site_name = getattr(settings, 'SITE_NAME', 'Site')
admin.site.site_header = site_name
admin.site.site_title = site_name
admin.site.index_title = f"Welcome to {site_name} admin"

