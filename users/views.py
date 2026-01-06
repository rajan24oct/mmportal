from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView, DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import UserProfile, ConnectionRequest, Message
from .forms import UserProfileForm
from posts.models import Post

User = get_user_model()

def profile_redirect(request):
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        url = reverse('users:profile_about', kwargs={'pk': profile.pk})
        if request.GET:
            url = f"{url}?{request.GET.urlencode()}"
        return redirect(url)
    return redirect('account_login')

class ProfileAboutUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'pages/my-profile-about-edit.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy('users:profile_about', kwargs={'pk': self.object.pk})

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    context_object_name = 'profile'

    def get_template_names(self):
        section = self.request.GET.get('section', 'about')
        if section == 'posts':
            return ['pages/my-profile.html']
        elif section == 'connections':
            return ['pages/my-profile-connections.html']
        elif section == 'media':
            return ['pages/my-profile-media.html']
        elif section == 'videos':
            return ['pages/my-profile-videos.html']
        return ['pages/my-profile-about.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        
        # Connections
        sent_requests = ConnectionRequest.objects.filter(sender=user, status='accepted')
        received_requests = ConnectionRequest.objects.filter(recipient=user, status='accepted')
        
        connections = []
        for req in sent_requests:
            connections.append(req.recipient)
        for req in received_requests:
            connections.append(req.sender)
        
        context['connections'] = connections[:10] # Initial load
        context['connection_count'] = len(connections)
        
        # Posts and Media
        user_posts = Post.objects.filter(author=user).order_by('-created_at')
        context['posts'] = user_posts
        context['media'] = user_posts.filter(image__isnull=False).exclude(image='')
        context['videos'] = user_posts.filter(video__isnull=False).exclude(video='')
        
        # Connection status with viewer
        if self.request.user != user:
            context['connection_request'] = ConnectionRequest.objects.filter(
                (Q(sender=self.request.user) & Q(recipient=user)) |
                (Q(sender=user) & Q(recipient=self.request.user))
            ).first()
            
        return context

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'pages/messaging.html'
    context_object_name = 'messages'

    def get_queryset(self):
        # List all connections for messaging sidebar
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique conversation partners
        user = self.request.user
        partners = User.objects.filter(
            Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
        ).distinct()
        context['partners'] = partners
        return context

class MessageDetailView(LoginRequiredMixin, View):
    def get(self, request, partner_pk):
        partner = get_object_or_404(User, pk=partner_pk)
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=partner)) |
            (Q(sender=partner) & Q(recipient=request.user))
        ).order_by('created_at')
        
        # Mark as read
        messages.filter(recipient=request.user, is_read=False).update(is_read=True)
        
        partners = User.objects.filter(
            Q(sent_messages__recipient=request.user) | Q(received_messages__sender=request.user)
        ).distinct()

        return render(request, 'pages/messaging-detail.html', {
            'partner': partner,
            'messages': messages,
            'partners': partners,
        })

    def post(self, request, partner_pk):
        partner = get_object_or_404(User, pk=partner_pk)
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=partner, content=content)
        return redirect('users:message_detail', partner_pk=partner_pk)


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


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import UserSettingsForm

class SettingsView(LoginRequiredMixin, View):
    template_name = 'pages/settings.html'

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        settings_form = UserSettingsForm(instance=profile)
        password_form = PasswordChangeForm(user=request.user)
        
        context = {
            'settings_form': settings_form,
            'password_form': password_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if 'account_settings' in request.POST:
            settings_form = UserSettingsForm(request.POST, request.FILES, instance=profile)
            password_form = PasswordChangeForm(user=request.user)
            
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, 'Account settings updated successfully.')
                return redirect('users:settings')
                
        elif 'password_change' in request.POST:
            settings_form = UserSettingsForm(instance=profile)
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Password updated successfully.')
                return redirect('users:settings')
        else:
             # Default fallback if something weird happens
            settings_form = UserSettingsForm(instance=profile)
            password_form = PasswordChangeForm(user=request.user)

        context = {
            'settings_form': settings_form,
            'password_form': password_form,
        }
        return render(request, self.template_name, context)
