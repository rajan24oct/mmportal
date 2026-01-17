
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from posts.models import Post
from users.models import UserProfile, ConnectionRequest


@login_required
def root_page_view(request):
    try:
        user = request.user
        
        # 1. Fetch Posts (User's posts + Connections' posts)
        # Find accepted connections
        sent_requests = ConnectionRequest.objects.filter(sender=user, status='accepted').values_list('recipient', flat=True)
        received_requests = ConnectionRequest.objects.filter(recipient=user, status='accepted').values_list('sender', flat=True)
        connected_user_ids = list(sent_requests) + list(received_requests)
        
        # Include the user's own ID
        author_ids = connected_user_ids + [user.id]
        
        posts = Post.objects.filter(author__id__in=author_ids).select_related('author', 'author__profile').order_by('-created_at')

        # 2. Fetch Suggested Mentors (Not connected, User type 'mentor')
        # Exclude already connected users and the current user
        suggested_mentors = UserProfile.objects.filter(user_type='mentor') \
                                               .exclude(user__id__in=connected_user_ids) \
                                               .exclude(user=user)[:5] # Limit to 5

        context = {
            'posts': posts,
            'suggested_mentors': suggested_mentors,
        }

        return render(request, 'pages/index.html', context)
    except TemplateDoesNotExist:
        return render(request, 'pages/pages-404.html')


def dynamic_pages_view(request, template_name):
    try:
        return render(request, f'pages/{template_name}.html')
    except TemplateDoesNotExist:
        return render(request, f'pages/pages-404.html')
