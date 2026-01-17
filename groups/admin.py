from django.contrib import admin
from .models import Group, GroupMembership, GroupMessage, GroupComment

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'moderator', 'unique_code', 'created_at')
    search_fields = ('name', 'unique_code')

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'status', 'joined_at')
    list_filter = ('status', 'group')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'content', 'created_at')
    list_filter = ('group', 'user')

@admin.register(GroupComment)
class GroupCommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'content', 'created_at')
