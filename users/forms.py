from allauth.account.forms import SignupForm
from django import forms
from .models import UserProfile

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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'dob', 'gender', 'marital_status', 'job_title', 
            'location', 'education_qualification', 'work_place'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
