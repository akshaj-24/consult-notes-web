from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import ApprovalAwareAuthenticationForm, SignupForm


class ApprovedLoginView(LoginView):
    form_class = ApprovalAwareAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if not self.request.user.is_approved:
            return reverse_lazy('accounts:awaiting_approval')
        return super().get_success_url()


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            'Account created. You can log in now, but an administrator must approve access first.',
        )
        return redirect(self.success_url)


class AwaitingApprovalView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/awaiting_approval.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_approved:
            return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)
