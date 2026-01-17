import os
import sys
import django

# Add the project directory to sys.path
sys.path.append('/opt/work/PycharmProjects/mmportal')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mmportal.settings')
django.setup()

from users.forms import UserSignupForm

try:
    form = UserSignupForm()
    print("Fields in form:", list(form.fields.keys()))
    if 'username' in form.fields:
        print("FAIL: username field is present")
    else:
        print("SUCCESS: username field is hidden")
except Exception as e:
    print(f"Error: {e}")
