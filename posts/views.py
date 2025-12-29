from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, Like

class PostCreateView(LoginRequiredMixin, View):
    def post(self, request):
        content = request.POST.get('content')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        if content or image or video:
            Post.objects.create(
                author=request.user,
                content=content,
                image=image,
                video=video
            )
        
        # Redirect back to the page they came from
        return redirect(request.META.get('HTTP_REFERER', 'users:profile_about', kwargs={'pk': request.user.profile.pk}))

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return redirect(request.META.get('HTTP_REFERER', 'users:profile_about', kwargs={'pk': request.user.profile.pk}))
