from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'mrn', 'cancer_site', 'disease_setting', 'consult_date', 'source_type')
    list_filter = ('source_type', 'cancer_site', 'disease_setting')
    search_fields = ('patient_name', 'mrn', 'cancer_site', 'synthetic_patient_id')
    readonly_fields = ('created_at', 'updated_at')
