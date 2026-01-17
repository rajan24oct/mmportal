from django.urls import path
from .views import (
    ProfileAboutUpdateView, 
    ProfileView,
    MentorListView,
    SendConnectionRequestView,
    AcceptConnectionRequestView,
    RejectConnectionRequestView,
    MessageListView,
    MessageDetailView,
    profile_redirect,
    SettingsView
)

app_name = 'users'

urlpatterns = [
    path('my-profile/', profile_redirect, name='profile_redirect'),
    path('my-profile-about-edit/', ProfileAboutUpdateView.as_view(), name='profile_about_edit'),
    path('my-profile-about/<str:pk>/', ProfileView.as_view(), name='profile_about'),
    path('mentors/', MentorListView.as_view(), name='mentor_list'),
    path('connect/<int:pk>/', SendConnectionRequestView.as_view(), name='send_connection_request'),
    path('connect/accept/<int:pk>/', AcceptConnectionRequestView.as_view(), name='accept_connection_request'),
    path('connect/reject/<int:pk>/', RejectConnectionRequestView.as_view(), name='reject_connection_request'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:partner_pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
