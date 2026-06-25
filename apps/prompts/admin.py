from django.contrib import admin

from .models import Prompt


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'prompt_type', 'is_active', 'updated_at')
    list_filter = ('prompt_type', 'is_active')
    search_fields = ('name', 'user__username', 'description')
