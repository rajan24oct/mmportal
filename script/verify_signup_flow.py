import os
import django
from django.test import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmportal.settings")
django.setup()

from invitations.models import Invitation
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.forms import UserSignupForm

def run_test():
    User = get_user_model()
    email = "test_invite_signup@example.com"
    
    # Clean up existing
    Invitation.objects.filter(email=email).delete()
    User.objects.filter(email=email).delete()
    
    print(f"Creating invitation for {email}...")
    invite = Invitation.create(email)
    invite.sent = timezone.now()
    invite.save()
    key = invite.key
    print(f"Invitation key: {key}")
    
    c = Client()
    
    # 1. Simulate clicking the invitation link
    # This should verify it redirects to signup
    # Note: `invitations` app handles this URL. 
    # django-invitations default URL is /invitations/accept-invite/<key>/
    url = f"/invitations/accept-invite/{key}/"
    print(f"Accessing URL: {url}")
    
    response = c.get(url, follow=True)
    print(f"Response status: {response.status_code}")
    
    # We expect to land on signup page
    # And there should be a signal/stash that creates the initial data for the form
    
    # 2. Check Form initialization (Unit Test style)
    # Simulate what happens when the form is instantiated with the session data
    # But doing this via Client is better to verify integration
    
    # Ideally, after clicking the link, the session is populated with the invitation email.
    # Let's check the session
    session = c.session
    print("Session Keys:", session.keys())
    
    # 3. Simulate Signup Submission
    # We need to submit the form. 
    # The form should auto-populate email and hide username.
    
    # Construct post data
    # Note: Using a fixed password
    submit_data = {
        'email': email,
        'password': 'StrongPassword123!@#', 
        'password1': 'StrongPassword123!@#',
        'password2': 'StrongPassword123!@#',
    }
    
    # The signup URL is likely /accounts/signup/
    signup_url = '/accounts/signup/'
    print(f"Submitting signup to {signup_url}")
    
    # We need to preserve the session from the previous request
    response = c.post(signup_url, submit_data, follow=True)
    print(f"Signup Response status: {response.status_code}")
    if response.context:
        print(f"Context Keys: {response.context.keys()}")
        if 'form' in response.context:
            print(f"Form Errors: {response.context['form'].errors}")
            print(f"Form Non Field Errors: {response.context['form'].non_field_errors()}")
    
    # Check for error in HTML content if context check fails
    content = response.content.decode('utf-8')
    if 'error' in content.lower() or 'invalid' in content.lower():
         # Simple grep for common error classes
         import re
         errors = re.findall(r'class="[^"]*error[^"]*"[^>]*>([^<]*)<', content)
         if errors:
             print(f"HTML Errors found: {errors}")
    
    with open('../debug_signup_response.html', 'w') as f:
        f.write(content)
    print("Dumped response to debug_signup_response.html")

    print(f"Redirect chain: {response.redirect_chain}")
    
    # Check if we landed on /my-profile/
    last_url = response.redirect_chain[-1][0] if response.redirect_chain else "No redirect"
    print(f"Final URL: {last_url}")
    
    if '/my-profile/' in last_url:
        print("SUCCESS: Redirected to /my-profile/")
    else:
        print(f"WARNING: Final URL check failed. Got {last_url}")

    # Check User
    try:
        user = User.objects.get(email=email)
        print("SUCCESS: User created")
        if user.username == email:
            print("SUCCESS: Username is email")
        else:
            print(f"FAILED: Username mismatch. Got {user.username}")
    except User.DoesNotExist:
        print("FAILED: User not created")

    # Check Login
    if '_auth_user_id' in c.session:
        print(f"SUCCESS: User logged in (User ID: {c.session['_auth_user_id']})")
    else:
        print("FAILED: User not logged in")

if __name__ == "__main__":
    run_test()
