from django.contrib import admin

from .models import User, UserConfirmation

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'auth_type', 'auth_status')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_active', 'is_staff', 'role', 'gender')

@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verify_type', 'is_confirmed')
    search_fields = ('user__username', 'verify_type', 'code')
    list_filter = ('verify_type', 'is_confirmed')