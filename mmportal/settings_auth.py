# django-allauth
ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_ADAPTER = "social.users.adapters.AccountAdapter"
# ACCOUNT_FORMS = {"signup": "social.users.forms.UserSignupForm"}
# SOCIALACCOUNT_ADAPTER = "social.users.adapters.SocialAccountAdapter"
SOCIALACCOUNT_FORMS = {"signup": "social.users.forms.UserSocialSignupForm"}