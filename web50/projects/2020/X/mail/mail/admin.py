from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Email

# Custom UserAdmin
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the User model with the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

# Custom EmailAdmin
class EmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'subject', 'timestamp', 'read', 'archived')
    list_filter = ('user', 'sender', 'read', 'archived')
    search_fields = ('user__username', 'sender__username', 'subject')

# Register the Email model with the custom EmailAdmin
admin.site.register(Email, EmailAdmin)
