from django.contrib import admin

from .models import GenerationSession


@admin.register(GenerationSession)
class GenerationSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'selected_patient', 'selected_model', 'updated_at')
    search_fields = ('user__username', 'selected_patient__patient_name', 'selected_patient__mrn')
    readonly_fields = ('created_at', 'updated_at')
