from django.urls import path

from .views import NoteFormatActivateView, NoteFormatCopyView, NoteFormatCreateView, NoteFormatDeleteView, NoteFormatListView, NoteFormatUpdateView

app_name = 'formats'

urlpatterns = [
    path('', NoteFormatListView.as_view(), name='list'),
    path('create/', NoteFormatCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', NoteFormatUpdateView.as_view(), name='edit'),
    path('<int:pk>/copy/', NoteFormatCopyView.as_view(), name='copy'),
    path('<int:pk>/activate/', NoteFormatActivateView.as_view(), name='activate'),
    path('<int:pk>/delete/', NoteFormatDeleteView.as_view(), name='delete'),
]
