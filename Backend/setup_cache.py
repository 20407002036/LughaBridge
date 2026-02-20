#!/usr/bin/env python3
"""
Setup HuggingFace cache - download only small config files
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

from huggingface_hub import hf_hub_download
from django.conf import settings

# Files to download for each model (small config files only, skip large model files)
model_files = {
    'facebook/wav2vec2-large-960h-lv60-self': [
        'config.json', 'preprocessor_config.json', 'special_tokens_map.json',
        'tokenizer_config.json', 'vocab.json'
    ],
    'facebook/nllb-200-distilled-600M': [
        'config.json', 'generation_config.json', 'sentencepiece.bpe.model',
        'special_tokens_map.json', 'tokenizer_config.json', 'tokenizer.json'
    ],
    'facebook/mms-tts-kik': [
        'config.json', 'vocab.txt'
    ],
    'facebook/mms-tts-eng': [
        'config.json', 'vocab.txt'
    ],
}

print("Downloading config files...")
print(f"Cache directory: {settings.HF_CACHE_DIR}\n")

for model_id, files in model_files.items():
    print(f"\n{model_id}:")
    for filename in files:
        try:
            path = hf_hub_download(
                repo_id=model_id,
                filename=filename,
                cache_dir=settings.HF_CACHE_DIR,
                token=settings.HF_TOKEN
            )
            print(f"  ✓ {filename}")
        except Exception as e:
            print(f"  ✗ {filename}: {e}")

print("\n✓ Config files downloaded!")
