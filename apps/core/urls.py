from django.urls import path

from .views import DashboardView, HomeView, ImportPatientSeedView, RefreshModelCatalogView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/import-patient-seed/', ImportPatientSeedView.as_view(), name='import_patient_seed'),
    path('dashboard/refresh-model-catalog/', RefreshModelCatalogView.as_view(), name='refresh_model_catalog'),
]
