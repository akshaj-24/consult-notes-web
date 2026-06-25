from django.urls import path

from .views import PromptActivateView, PromptCopyView, PromptCreateView, PromptDeleteView, PromptListView, PromptUpdateView

app_name = 'prompts'

urlpatterns = [
    path('', PromptListView.as_view(), name='list'),
    path('create/', PromptCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', PromptUpdateView.as_view(), name='edit'),
    path('<int:pk>/copy/', PromptCopyView.as_view(), name='copy'),
    path('<int:pk>/activate/', PromptActivateView.as_view(), name='activate'),
    path('<int:pk>/delete/', PromptDeleteView.as_view(), name='delete'),
]
