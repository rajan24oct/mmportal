from django.urls import path
from .views import PostCreateView, LikePostView

app_name = 'posts'

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('like/<int:pk>/', LikePostView.as_view(), name='like_post'),
]
