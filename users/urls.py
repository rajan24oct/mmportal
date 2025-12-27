from django.urls import path
from .views import (
    ProfileAboutUpdateView, 
    ProfileAboutDetailView,
    MentorListView,
    SendConnectionRequestView,
    AcceptConnectionRequestView,
    RejectConnectionRequestView
)

app_name = 'users'

urlpatterns = [
    path('my-profile-about-edit/', ProfileAboutUpdateView.as_view(), name='profile_about_edit'),
    path('my-profile-about/<str:pk>/', ProfileAboutDetailView.as_view(), name='profile_about'),
    path('mentors/', MentorListView.as_view(), name='mentor_list'),
    path('connect/<int:pk>/', SendConnectionRequestView.as_view(), name='send_connection_request'),
    path('connect/accept/<int:pk>/', AcceptConnectionRequestView.as_view(), name='accept_connection_request'),
    path('connect/reject/<int:pk>/', RejectConnectionRequestView.as_view(), name='reject_connection_request'),
]
