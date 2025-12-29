import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
import uuid
from invitations.models import AbstractBaseInvitation
from invitations.adapters import get_invitations_adapter
from invitations.app_settings import app_settings

GENDER_CHOICES = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other')
)
MARITAL_STATUS = (
    ('Single','Single'),
    ('Married','Married'),
    ('Divorced','Divorced'),
    ('Separated','Separated'),
    ('Widowed','Widowed'),
)


class Invitation(AbstractBaseInvitation):
    email = models.EmailField(
        unique=True,
        verbose_name=_("e-mail address"),
        max_length=getattr(app_settings, 'EMAIL_MAX_LENGTH', 254),
    )
    created = models.DateTimeField(verbose_name=_("created"), default=timezone.now)
    
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("inviter"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='custom_invitations' # Avoid clash with invitations.Invitation
    )

    INVITATION_TYPES = (
        ('mentor', 'Mentor'),
        ('normal', 'Normal'),
    )
    invitation_type = models.CharField(
        max_length=10,
        choices=INVITATION_TYPES,
        default='normal'
    )

    @classmethod
    def create(cls, email, inviter=None, **kwargs):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email, key=key, inviter=inviter, **kwargs
        )
        return instance

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            days=app_settings.INVITATION_EXPIRY,
        )
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        from django.contrib.sites.shortcuts import get_current_site
        try:
            from django.urls import reverse
        except ImportError:
            from django.core.urlresolvers import reverse
            
        current_site = get_current_site(request)
        invite_url = reverse(app_settings.CONFIRMATION_URL_NAME, args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update(
            {
                "invite_url": invite_url,
                "site_name": current_site.name,
                "email": self.email,
                "key": self.key,
                "inviter": self.inviter,
            },
        )

        email_template = "invitations/email/email_invite"

        get_invitations_adapter().send_mail(email_template, self.email, ctx)
        self.sent = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.email} ({self.invitation_type})"

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    user_type = models.CharField(
        max_length=10,
        choices=Invitation.INVITATION_TYPES,
        default='normal'
    )
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, blank=True, null=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    education_qualification = models.CharField(max_length=100, null=True, blank=True)
    work_place = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.email} - {self.user_type}"


class ConnectionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'recipient')

    def __str__(self):
        return f"{self.sender.email} -> {self.recipient.email} ({self.status})"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"From {self.sender.email} to {self.recipient.email} at {self.created_at}"
