from django import forms
from django.contrib import admin
from invitations.admin import InvitationAdmin
from invitations.forms import CleanEmailMixin
from .models import Invitation, UserProfile, ConnectionRequest

class CustomInvitationAdminAddForm(forms.ModelForm, CleanEmailMixin):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.TextInput(attrs={"type": "email", "size": "30"}),
    )

    def save(self, *args, **kwargs):
        cleaned_data = self.cleaned_data # Use self.cleaned_data instead of re-cleaning
        email = cleaned_data.get("email")
        params = {
            "email": email,
            "invitation_type": cleaned_data.get("invitation_type"),
        }
        if cleaned_data.get("inviter"):
            params["inviter"] = cleaned_data.get("inviter")
        
        instance = Invitation.create(**params)
        instance.send_invitation(self.request)
        # super().save(*args, **kwargs) # Original calls this, but it might be confusing
        return instance

    def save_m2m(self):
        # We don't have any m2m fields to save, but Django Admin expects this method
        pass

    class Meta:
        model = Invitation
        fields = ("email", "inviter", "invitation_type")

# Unregister the default admin registered by django-invitations
try:
    admin.site.unregister(Invitation)
except admin.sites.NotRegistered:
    pass

@admin.register(Invitation)
class CustomInvitationAdmin(InvitationAdmin):
    list_display = ('email', 'invitation_type', 'sent', 'accepted', 'key')
    list_filter = ('invitation_type', 'sent', 'accepted')
    
    def get_form(self, request, obj=None, **kwargs):
        form_class = super().get_form(request, obj, **kwargs)
        if obj is None:
            # Ensure our custom form is used and has request/user
            CustomInvitationAdminAddForm.request = request
            CustomInvitationAdminAddForm.user = request.user
            return CustomInvitationAdminAddForm
        return form_class

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            # Flow 1: on invitation create it should show only email, invitation_type, inviter
            return (
                (None, {'fields': ('email', 'invitation_type', 'inviter')}),
            )
        # Flow 2: on edit it should show all the fields
        return (
            (None, {'fields': ('email', 'invitation_type', 'inviter', 'accepted', 'key', 'sent', 'created')}),
        )
    
    readonly_fields = ('key', 'sent', 'created')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('user__email',)

@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('sender__email', 'recipient__email')
