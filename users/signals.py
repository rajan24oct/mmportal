from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Invitation, UserProfile

@receiver(user_signed_up)
def assign_user_type(request, user, **kwargs):
    # Try to find an invitation for this user's email
    email = user.email
    invitation = Invitation.objects.filter(email__iexact=email).first()
    
    if invitation:
        user_type = invitation.invitation_type
    else:
        user_type = 'normal'
        
    UserProfile.objects.update_or_create(
        user=user,
        defaults={'user_type': user_type}
    )
