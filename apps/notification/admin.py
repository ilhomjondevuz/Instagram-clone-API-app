from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'recipient', 'is_read')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('notification_type', 'post__caption', 'comment__comment')