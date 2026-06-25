from django.urls import path

from .views import GenerateConsultNoteView, GenerationPatientSelectView, GenerationRandomPatientView, GenerationSetPatientView, GenerationSettingsView, GenerationSummaryView, StartGenerationView

app_name = 'generation'

urlpatterns = [
    path('start/', StartGenerationView.as_view(), name='start'),
    path('sessions/<int:pk>/patient/', GenerationPatientSelectView.as_view(), name='patient'),
    path('sessions/<int:pk>/patient/random/', GenerationRandomPatientView.as_view(), name='random_patient'),
    path('sessions/<int:pk>/patient/<int:patient_id>/', GenerationSetPatientView.as_view(), name='set_patient'),
    path('sessions/<int:pk>/settings/', GenerationSettingsView.as_view(), name='settings'),
    path('sessions/<int:pk>/summary/', GenerationSummaryView.as_view(), name='summary'),
    path('sessions/<int:pk>/generate/', GenerateConsultNoteView.as_view(), name='generate'),
]
