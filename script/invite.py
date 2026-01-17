from invitations.utils import get_invitation_model
Invitation = get_invitation_model()

email_address = "mentor1@example.com"
invitation = (Invitation.objects
    .filter(email__iexact=email_address)
    .order_by('created')
    .last()
)
if invitation is None:
    # Do not use Invitation.objects.create or
    # Invitation.objects.update_or_create, but use Invitation.create
    # instead, because it sets the key to a secure random value
    invitation = Invitation.create(email=email_address)


invitation.send_invitation()
