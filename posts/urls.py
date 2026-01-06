from django.urls import path
from .views import PostCreateView, LikePostView, PostCommentView

app_name = 'posts'

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('like/<int:pk>/', LikePostView.as_view(), name='like_post'),
    path('comment/<int:pk>/', PostCommentView.as_view(), name='post_comment'),
]

