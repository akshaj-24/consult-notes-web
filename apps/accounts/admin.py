from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_approved', 'is_staff', 'is_superuser', 'active_format', 'created_at')
    list_filter = ('is_approved', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('Consult Notes', {'fields': ('is_approved', 'active_format', 'created_at', 'updated_at')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Consult Notes', {'fields': ('is_approved',)}),
    )
