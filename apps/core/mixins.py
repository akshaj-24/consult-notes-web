from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class UserOwnedQuerysetMixin(LoginRequiredMixin):
    queryset_user_field = 'user'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(**{self.queryset_user_field: self.request.user})


class UserOwnedFormMixin(LoginRequiredMixin):
    def form_valid(self, form):
        if not getattr(form.instance, 'user_id', None):
            form.instance.user = self.request.user
        return super().form_valid(form)


class SuperuserRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('Only superusers can perform this action.')
        return super().dispatch(request, *args, **kwargs)
