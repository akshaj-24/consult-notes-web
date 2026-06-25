from django.contrib import admin

from .models import LLMModelConfig


@admin.register(LLMModelConfig)
class LLMModelConfigAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'provider', 'model_key', 'is_active', 'sort_order')
    list_filter = ('provider', 'is_active')
    search_fields = ('display_name', 'model_key')
