from django.contrib import admin

from .models import NoteFormat


@admin.register(NoteFormat)
class NoteFormatAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'user__username')
