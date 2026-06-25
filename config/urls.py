from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.core.urls')),
    path('patients/', include('apps.patients.urls')),
    path('prompts/', include('apps.prompts.urls')),
    path('formats/', include('apps.formats.urls')),
    path('generation/', include('apps.generation.urls')),
    path('consults/', include('apps.consults.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
