from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import UserProfile, ConnectionRequest
from .forms import UserProfileForm

User = get_user_model()

class ProfileAboutUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'pages/my-profile-about-edit.html'

    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy('users:profile_about', kwargs={'pk': self.object.pk})

class ProfileAboutDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'pages/my-profile-about.html'


class MentorListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'pages/mentor-list.html'
    context_object_name = 'mentors'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = UserProfile.objects.filter(user_type='mentor')
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(job_title__icontains=query) |
                Q(location__icontains=query)
            )
        return queryset

class SendConnectionRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        recipient = get_object_or_404(User, pk=pk)
        if recipient != request.user:
            ConnectionRequest.objects.get_or_create(sender=request.user, recipient=recipient)
        return redirect('users:mentor_list')

class AcceptConnectionRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        connection_request = get_object_or_404(ConnectionRequest, pk=pk, recipient=request.user)
        connection_request.status = 'accepted'
        connection_request.save()
        return redirect('users:profile_about', pk=request.user.profile.pk)

class RejectConnectionRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        connection_request = get_object_or_404(ConnectionRequest, pk=pk, recipient=request.user)
        connection_request.status = 'rejected'
        connection_request.save()
        return redirect('users:profile_about', pk=request.user.profile.pk)
