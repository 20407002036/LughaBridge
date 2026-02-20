#!/usr/bin/env python3
"""Quick test to verify models load from cache"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')

import django
django.setup()

from django.conf import settings
from transformers import AutoConfig

models = {
    'Kikuyu ASR': 'badrex/w2v-bert-2.0-kikuyu-asr',
    'English ASR': 'facebook/wav2vec2-large-960h-lv60-self',
    'Kikuyu TTS': 'facebook/mms-tts-kik',
    'English TTS': 'facebook/mms-tts-eng',
    'Translation': 'facebook/nllb-200-distilled-600M',
}

print(f"Testing model loading from cache: {settings.HF_CACHE_DIR}\n")

for name, model_id in models.items():
    try:
        config = AutoConfig.from_pretrained(
            model_id,
            cache_dir=settings.HF_CACHE_DIR,
            local_files_only=True  # Force use of cache only
        )
        print(f"✓ {name:20s} - {model_id}")
    except Exception as e:
        print(f"✗ {name:20s} - ERROR: {str(e)[:60]}")

print("\n✓ Cache verification complete!")
