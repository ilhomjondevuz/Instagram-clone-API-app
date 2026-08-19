from django.contrib import admin

from .models import SavedPost


@admin.register(SavedPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__username', 'post__caption', 'created_at', 'updated_at')
    list_filter = ('user__username', 'post__caption')
    search_fields = ('user__username', 'post__caption')