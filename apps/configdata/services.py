from __future__ import annotations

import csv
from pathlib import Path

from django.conf import settings

from .models import LLMModelConfig

DEFAULT_MODELS = [
    {
        'provider': 'local',
        'model_key': 'dummy-sample-note',
        'display_name': 'Dummy Sample Note Generator',
        'is_active': True,
        'supports_temperature': True,
        'supports_top_p': True,
        'supports_max_tokens': True,
        'supports_system_prompt': True,
        'supports_streaming': False,
        'sort_order': 1,
    }
]


def _to_bool(value: str) -> bool:
    return str(value).strip().lower() in {'1', 'true', 'yes', 'y'}


def import_model_configs(csv_path: Path | None = None):
    csv_path = csv_path or settings.BASE_DIR / 'data' / 'llm_models.csv'
    created = 0
    updated = 0
    rows = []
    if csv_path.exists():
        with csv_path.open(newline='', encoding='utf-8-sig') as handle:
            rows = [row for row in csv.DictReader(handle) if any((value or '').strip() for value in row.values())]
    if not rows:
        rows = DEFAULT_MODELS

    for row in rows:
        defaults = {
            'provider': row['provider'],
            'display_name': row['display_name'],
            'is_active': row['is_active'] if isinstance(row['is_active'], bool) else _to_bool(row['is_active']),
            'supports_temperature': row['supports_temperature'] if isinstance(row['supports_temperature'], bool) else _to_bool(row['supports_temperature']),
            'supports_top_p': row['supports_top_p'] if isinstance(row['supports_top_p'], bool) else _to_bool(row['supports_top_p']),
            'supports_max_tokens': row['supports_max_tokens'] if isinstance(row['supports_max_tokens'], bool) else _to_bool(row['supports_max_tokens']),
            'supports_system_prompt': row['supports_system_prompt'] if isinstance(row['supports_system_prompt'], bool) else _to_bool(row['supports_system_prompt']),
            'supports_streaming': row['supports_streaming'] if isinstance(row['supports_streaming'], bool) else _to_bool(row['supports_streaming']),
            'sort_order': int(row.get('sort_order', 0) or 0),
        }
        _, was_created = LLMModelConfig.objects.update_or_create(model_key=row['model_key'], defaults=defaults)
        if was_created:
            created += 1
        else:
            updated += 1
    return created, updated
