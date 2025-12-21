from allauth.account.forms import SignupForm

class UserSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        
        # Try to handle email locking
        email = self.initial.get('email')
        if email:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['email'].help_text = "Your email is locked to the invitation."

    def save(self, request):
        # allauth will handle username generation because 
        # ACCOUNT_AUTHENTICATION_METHOD="email" and ACCOUNT_USERNAME_REQUIRED=False
        user = super(UserSignupForm, self).save(request)
        return user
