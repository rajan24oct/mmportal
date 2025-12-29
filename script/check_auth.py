import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmportal.settings')
django.setup()

from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django.conf import settings

User = get_user_model()

print(f"AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")
print(f"SITE_ID: {getattr(settings, 'SITE_ID', 'Missing')}")
print(f"INSTALLED_APPS (sites): {'django.contrib.sites' in settings.INSTALLED_APPS}")

users = User.objects.all()
print(f"\nTotal users: {users.count()}")
for user in users:
    email_records = EmailAddress.objects.filter(user=user)
    print(f"User: {user.email} (ID: {user.pk})")
    if email_records.exists():
        for er in email_records:
            print(f"  - allauth email: {er.email} (Verified: {er.verified})")
    else:
        print("  - NO allauth EmailAddress record found!")
