from __future__ import annotations

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.core.mixins import SuperuserRequiredMixin, UserOwnedFormMixin, UserOwnedQuerysetMixin

from .forms import PromptForm
from .models import Prompt


class PromptListView(UserOwnedQuerysetMixin, ListView):
    model = Prompt
    template_name = 'prompts/prompt_list.html'
    context_object_name = 'prompts'


class PromptCreateView(UserOwnedFormMixin, CreateView):
    model = Prompt
    form_class = PromptForm
    template_name = 'prompts/prompt_form.html'

    def get_success_url(self):
        return reverse('prompts:list')


class PromptUpdateView(UserOwnedQuerysetMixin, UserOwnedFormMixin, UpdateView):
    model = Prompt
    form_class = PromptForm
    template_name = 'prompts/prompt_form.html'

    def get_success_url(self):
        return reverse('prompts:list')


class PromptCopyView(UserOwnedQuerysetMixin, CreateView):
    model = Prompt
    form_class = PromptForm
    template_name = 'prompts/prompt_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.source_prompt = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'name': f'{self.source_prompt.name} Copy',
            'prompt_type': self.source_prompt.prompt_type,
            'description': self.source_prompt.description,
            'content': self.source_prompt.content,
            'is_active': False,
        }

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Prompt copied.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('prompts:list')


class PromptActivateView(UserOwnedQuerysetMixin, View):
    def post(self, request, *args, **kwargs):
        prompt = get_object_or_404(Prompt.objects.filter(user=request.user), pk=kwargs['pk'])
        prompt.is_active = True
        prompt.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, f'{prompt.name} is now the active {prompt.get_prompt_type_display().lower()} prompt.')
        return redirect('prompts:list')


class PromptDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        prompt = get_object_or_404(Prompt, pk=kwargs['pk'])
        prompt_name = prompt.name
        prompt.delete()
        messages.success(request, f'{prompt_name} was deleted.')
        return redirect('prompts:list')
