from django.urls import path

from .views import ConsultDeleteView, ConsultNoteListView, ConsultRegenerateView, ConsultReviewAutosaveView, LoadSettingsFromConsultView

app_name = 'consults'

urlpatterns = [
    path('', ConsultNoteListView.as_view(), name='list'),
    path('<int:pk>/', ConsultNoteListView.as_view(), name='detail'),
    path('<int:pk>/autosave/', ConsultReviewAutosaveView.as_view(), name='autosave'),
    path('<int:pk>/regenerate/', ConsultRegenerateView.as_view(), name='regenerate'),
    path('<int:pk>/load-settings/', LoadSettingsFromConsultView.as_view(), name='load_settings'),
    path('<int:pk>/delete/', ConsultDeleteView.as_view(), name='delete'),
]
