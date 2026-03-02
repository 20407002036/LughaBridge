#!/usr/bin/env python
"""Simple test to verify HF Inference API works."""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

#!/usr/bin/env python
"""
Test translation backends:
  - HF NLLB (facebook/nllb-200-distilled-600M) → Kikuyu ↔ English
  - Groq (llama-3.3-70b-versatile)             → Swahili ↔ English
  - HybridTranslator via ModelFactory           → full routing
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

from django.conf import settings

PASS = "✓"
FAIL = "✗"

def section(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)

def run_test(label, fn):
    try:
        result = fn()
        print(f"  {PASS} {label}: {result}")
        return True
    except Exception as e:
        print(f"  {FAIL} {label}: {type(e).__name__}: {e}")
        return False

# ------------------------------------------------------------------
# 1.  HF NLLB – Kikuyu translations
# ------------------------------------------------------------------
section("1. HF NLLB — STATUS CHECK (HF removed free-tier translation hosting March 2026)")
print(f"  Model   : {settings.MODELS['translation']['model']}")
print(f"  Endpoint: https://router.huggingface.co/hf-inference/models/...")
print(f"  Status  : KNOWN 404 — HF no longer hosts NLLB on free inference API.")
print(f"  Action  : Groq (section 3) is primary. HF kept as fallback if restored.\n")

# Confirm the 404 is consistent
from translation.services.hf_inference_services import HFInferenceTranslator
hf = HFInferenceTranslator()
r = run_test("HF NLLB EN→KIK  (expected 404)", lambda: hf.translate("Hello", "english", "kikuyu")["text"])
if not r:
    print("  → Confirmed dead. System falls back to Groq automatically.")

# ------------------------------------------------------------------
# 2.  Groq LLM – Swahili translations
# ------------------------------------------------------------------
section("2. Groq (llama-3.3-70b-versatile) — Swahili")
print(f"  Model: {settings.GROQ_MODEL}")
print(f"  Key  : {settings.GROQ_API_KEY[:20]}...")

from translation.services.groq_translator import GroqTranslator
groq = GroqTranslator()

run_test("EN→SW   'Hello, how are you?'",
         lambda: groq.translate("Hello, how are you?", "english", "swahili")["text"])
run_test("SW→EN   'Habari yako?'",
         lambda: groq.translate("Habari yako?", "swahili", "english")["text"])
run_test("SW→EN   'Karibu Kenya'",
         lambda: groq.translate("Karibu Kenya", "swahili", "english")["text"])

# ------------------------------------------------------------------
# 3.  HybridTranslator via ModelFactory  (full routing check)
# ------------------------------------------------------------------
section("3. ModelFactory → HybridTranslator (routing check)")

from translation.services.factory import ModelFactory
svc = ModelFactory.get_translation_service()
print(f"  Service: {type(svc).__name__}")

pairs = [
    ("Good morning",        "english", "kikuyu"),
    ("Nĩ wega",             "kikuyu",  "english"),
    ("Good morning",        "english", "swahili"),
    ("Habari za asubuhi",   "swahili", "english"),
]

for text, src, tgt in pairs:
    try:
        r = svc.translate(text, src, tgt)
        via = r.get("service_used", "?")
        print(f"  {PASS} [{src:7s}→{tgt:7s}] {text!r:30s} => {r['text']!r}  (via {via})")
    except Exception as e:
        print(f"  {FAIL} [{src}→{tgt}] {text!r}: {e}")

print()

