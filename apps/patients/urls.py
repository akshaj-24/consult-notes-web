from django.urls import path

from .views import (
    PatientCopyView,
    PatientCreateView,
    PatientDeleteView,
    PatientDetailView,
    PatientListView,
    PatientUpdateView,
    RandomPatientRedirectView,
)

app_name = 'patients'

urlpatterns = [
    path('', PatientListView.as_view(), name='list'),
    path('random/', RandomPatientRedirectView.as_view(), name='random'),
    path('create/', PatientCreateView.as_view(), name='create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', PatientUpdateView.as_view(), name='edit'),
    path('<int:pk>/copy/', PatientCopyView.as_view(), name='copy'),
    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='delete'),
]
