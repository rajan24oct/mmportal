ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_ADAPTER = "social.users.adapters.AccountAdapter"
# ACCOUNT_FORMS = {"signup": "social.users.forms.UserSignupForm"}
# SOCIALACCOUNT_ADAPTER = "social.users.adapters.SocialAccountAdapter"
SOCIALACCOUNT_FORMS = {"signup": "social.users.forms.UserSocialSignupForm"}
ACCOUNT_FORMS = {"signup": "users.forms.UserSignupForm"}

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# django-allauth configuration:
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"

# django-invitations configuration:
INVITATIONS_ADAPTER = ACCOUNT_ADAPTER
INVITATIONS_INVITATION_ONLY = True
INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
INVITATIONS_INVITATION_MODEL = 'users.Invitation'
INVITATIONS_LOGIN_REDIRECT = "my-profile/"
LOGIN_REDIRECT_URL = "/my-profile/"