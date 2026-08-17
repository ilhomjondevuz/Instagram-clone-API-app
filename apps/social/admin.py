from django.contrib import admin

from .models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('follower__username', 'following__username')
    ordering = ('-created_at',)