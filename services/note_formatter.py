from __future__ import annotations

from django.utils.html import escape


def render_note_html(note_text: str) -> str:
    lines = [line.rstrip() for line in (note_text or '').splitlines()]
    html = []
    in_list = False
    for line in lines:
        if not line.strip():
            if in_list:
                html.append('</ul>')
                in_list = False
            continue
        if line.startswith('-- '):
            if not in_list:
                html.append('<ul>')
                in_list = True
            html.append(f'<li>{escape(line[3:])}</li>')
            continue
        if in_list:
            html.append('</ul>')
            in_list = False
        if line.isupper() and len(line) <= 80:
            html.append(f'<h5 class="mt-4">{escape(line)}</h5>')
        else:
            html.append(f'<p>{escape(line)}</p>')
    if in_list:
        html.append('</ul>')
    return ''.join(html)
