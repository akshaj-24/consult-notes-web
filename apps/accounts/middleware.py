from __future__ import annotations

from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class ApprovalRequiredMiddleware(MiddlewareMixin):
    public_view_names = {
        'accounts:login',
        'accounts:logout',
        'accounts:signup',
        'accounts:awaiting_approval',
    }

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated or user.is_approved or user.is_superuser or user.is_staff:
            return None

        if request.path.startswith('/admin/'):
            return None

        if settings.STATIC_URL and request.path.startswith(settings.STATIC_URL):
            return None

        if settings.MEDIA_URL and request.path.startswith(settings.MEDIA_URL):
            return None

        if request.resolver_match and request.resolver_match.view_name in self.public_view_names:
            return None

        return redirect('accounts:awaiting_approval')
