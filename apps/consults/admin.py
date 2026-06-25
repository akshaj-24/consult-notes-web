from django.contrib import admin

from .models import ConsultNote


@admin.register(ConsultNote)
class ConsultNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'patient', 'status', 'llm_model_key', 'updated_at')
    list_filter = ('status', 'llm_model_key')
    search_fields = ('title', 'patient__patient_name', 'patient__mrn', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
