from __future__ import annotations

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from apps.core.mixins import SuperuserRequiredMixin, UserOwnedFormMixin, UserOwnedQuerysetMixin

from .forms import NoteFormatForm
from .models import NoteFormat


class NoteFormatListView(UserOwnedQuerysetMixin, ListView):
    model = NoteFormat
    template_name = 'formats/format_list.html'
    context_object_name = 'formats'


class NoteFormatCreateView(UserOwnedFormMixin, CreateView):
    model = NoteFormat
    form_class = NoteFormatForm
    template_name = 'formats/format_form.html'

    def get_success_url(self):
        return reverse('formats:list')


class NoteFormatUpdateView(UserOwnedQuerysetMixin, UserOwnedFormMixin, UpdateView):
    model = NoteFormat
    form_class = NoteFormatForm
    template_name = 'formats/format_form.html'

    def get_success_url(self):
        return reverse('formats:list')


class NoteFormatCopyView(UserOwnedQuerysetMixin, CreateView):
    model = NoteFormat
    form_class = NoteFormatForm
    template_name = 'formats/format_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.source_format = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'name': f'{self.source_format.name} Copy',
            'is_active': False,
            'heading_font_family': self.source_format.heading_font_family,
            'heading_font_size': self.source_format.heading_font_size,
            'heading_bold': self.source_format.heading_bold,
            'subheading_font_family': self.source_format.subheading_font_family,
            'subheading_font_size': self.source_format.subheading_font_size,
            'subheading_bold': self.source_format.subheading_bold,
            'body_font_family': self.source_format.body_font_family,
            'body_font_size': self.source_format.body_font_size,
            'body_bold': self.source_format.body_bold,
            'show_lines_between_sections': self.source_format.show_lines_between_sections,
            'section_spacing': self.source_format.section_spacing,
            'left_margin': self.source_format.left_margin,
            'right_margin': self.source_format.right_margin,
            'top_margin': self.source_format.top_margin,
            'bottom_margin': self.source_format.bottom_margin,
            'header_text': self.source_format.header_text,
            'footer_text': self.source_format.footer_text,
            'template_style_json': self.source_format.template_style_json,
        }

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Format copied.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('formats:list')


class NoteFormatActivateView(UserOwnedQuerysetMixin, View):
    def post(self, request, *args, **kwargs):
        note_format = get_object_or_404(NoteFormat.objects.filter(user=request.user), pk=kwargs['pk'])
        note_format.is_active = True
        note_format.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, f'{note_format.name} is now your active format.')
        return redirect('formats:list')


class NoteFormatDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note_format = get_object_or_404(NoteFormat, pk=kwargs['pk'])
        format_name = note_format.name
        note_format.delete()
        messages.success(request, f'{format_name} was deleted.')
        return redirect('formats:list')
