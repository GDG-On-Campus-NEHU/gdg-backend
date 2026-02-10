import os
import secrets
import sys
from pathlib import Path

# Ensure project root is on sys.path so Django project imports work when running this script directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_core.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

pwd = secrets.token_urlsafe(12)

su = User.objects.filter(is_superuser=True).first()
if su:
    su.set_password(pwd)
    su.save()
    print('RESET_SUPERUSER', su.username, pwd)
else:
    username = 'admin'
    email = 'admin@example.com'
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
        u.set_password(pwd)
        u.is_superuser = True
        u.is_staff = True
        u.email = email
        u.save()
        print('UPDATED_EXISTING', username, pwd)
    else:
        User.objects.create_superuser(username, email, pwd)
        print('CREATED', username, pwd)
