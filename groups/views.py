from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from .models import Group, GroupMembership, GroupMessage, GroupComment

User = get_user_model()

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups/group_list.html'
    context_object_name = 'groups'

class GroupJoinRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        GroupMembership.objects.get_or_create(group=group, user=request.user)
        return redirect('groups:group_list')

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_messages = self.object.messages.all().order_by('-created_at')
        context['group_messages'] = group_messages
        context['members'] = self.object.memberships.filter(status='approved')
        context['pending_members'] = self.object.memberships.filter(status='pending')
        context['media'] = group_messages.filter(image__isnull=False).exclude(image='')
        context['videos'] = group_messages.filter(video__isnull=False).exclude(video='')
        context['is_member'] = self.object.memberships.filter(user=self.request.user, status='approved').exists()
        context['is_moderator'] = self.object.moderator == self.request.user
        return context

class GroupModerationView(LoginRequiredMixin, View):
    def post(self, request, pk, action):
        membership = get_object_or_404(GroupMembership, pk=pk, group__moderator=request.user)
        if action == 'approve':
            membership.status = 'approved'
            membership.save()
        elif action == 'reject':
            membership.delete()
        return redirect('groups:group_detail', pk=membership.group.pk)

class PostGroupMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        if group.memberships.filter(user=request.user, status='approved').exists() or group.moderator == request.user:
            content = request.POST.get('content')
            image = request.FILES.get('image')
            video = request.FILES.get('video')
            GroupMessage.objects.create(group=group, user=request.user, content=content, image=image, video=video)
        return redirect('groups:group_detail', pk=pk)

class LikeGroupMessageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        message = get_object_or_404(GroupMessage, pk=pk)
        if request.user in message.likes.all():
            message.likes.remove(request.user)
        else:
            message.likes.add(request.user)
        return redirect('groups:group_detail', pk=message.group.pk)

class GroupCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        message = get_object_or_404(GroupMessage, pk=pk)
        content = request.POST.get('content')
        if content:
            GroupComment.objects.create(message=message, user=request.user, content=content)
        return redirect('groups:group_detail', pk=message.group.pk)

