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
            'location', 'education_qualification', 'work_place', 'about', 'profile_picture'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = [
            'dob', 'gender', 'marital_status', 'job_title', 
            'location', 'education_qualification', 'work_place', 'about', 'profile_picture'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile.save()
        return profile
