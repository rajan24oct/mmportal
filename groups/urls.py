from django.urls import path
from .views import (
    GroupListView,
    GroupJoinRequestView,
    GroupDetailView,
    GroupModerationView,
    PostGroupMessageView,
    LikeGroupMessageView
)

app_name = 'groups'

urlpatterns = [
    path('', GroupListView.as_view(), name='group_list'),
    path('join/<int:pk>/', GroupJoinRequestView.as_view(), name='group_join'),
    path('<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path('moderate/<int:pk>/<str:action>/', GroupModerationView.as_view(), name='group_moderate'),
    path('<int:pk>/post/', PostGroupMessageView.as_view(), name='post_message'),
    path('message/like/<int:pk>/', LikeGroupMessageView.as_view(), name='like_message'),
]
