#!/usr/bin/env python3
"""
Test script for hybrid translation system.
Tests Groq + HuggingFace hybrid routing and fallback mechanisms.

Usage:
    python test_hybrid_translation.py
    
Environment variables:
    GROQ_API_KEY - Groq API key (optional, system uses HF if not provided)
    HF_TOKEN - HuggingFace token (required for HF Inference API)
    USE_HF_INFERENCE - Set to True to use cloud APIs
"""

import os
import sys
import time
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

from django.conf import settings
from translation.services.factory import ModelFactory
from translation.services.hybrid_translator import HybridTranslator


def print_header(text):
    """Print formatted header."""
    print(f"\n{'=' * 80}")
    print(f"  {text}")
    print(f"{'=' * 80}\n")


def print_config():
    """Print current configuration."""
    print_header("CONFIGURATION")
    
    print(f"🔧 USE_HF_INFERENCE: {settings.USE_HF_INFERENCE}")
    print(f"🔧 DEMO_MODE: {settings.DEMO_MODE}")
    print(f"🔧 SUPPORTED_LANGUAGES: {', '.join(settings.SUPPORTED_LANGUAGES)}")
    
    # Check API keys
    groq_key = getattr(settings, 'GROQ_API_KEY', '')
    hf_token = getattr(settings, 'HF_TOKEN', '')
    
    print(f"\n🔑 GROQ_API_KEY: {'✓ Set' if groq_key and groq_key.strip() else '✗ Not set'}")
    if groq_key and groq_key.strip():
        print(f"   Model: {getattr(settings, 'GROQ_MODEL', 'default')}")
        print(f"   Key: {groq_key[:10]}...{groq_key[-4:] if len(groq_key) > 14 else ''}")
    
    print(f"🔑 HF_TOKEN: {'✓ Set' if hf_token and hf_token.strip() else '✗ Not set'}")
    if hf_token and hf_token.strip():
        print(f"   Token: {hf_token[:10]}...{hf_token[-4:] if len(hf_token) > 14 else ''}")


def test_translation(translator, text, source_lang, target_lang):
    """
    Test a single translation and return results.
    
    Args:
        translator: Translation service instance
        text: Text to translate
        source_lang: Source language code
        target_lang: Target language code
        
    Returns:
        dict: Test results with timing and metadata
    """
    print(f"\n📝 Testing: {source_lang.upper()} → {target_lang.upper()}")
    print(f"   Input: '{text}'")
    
    try:
        start_time = time.time()
        result = translator.translate(text, source_lang, target_lang)
        duration = time.time() - start_time
        
        translated_text = result.get('text', '')
        confidence = result.get('confidence', 0.0)
        service_used = result.get('service_used', 'unknown')
        is_fallback = result.get('fallback', False)
        
        print(f"   Output: '{translated_text}'")
        print(f"   ✓ Service: {service_used.upper()}", end='')
        if is_fallback:
            print(" (fallback)", end='')
        print()
        print(f"   ⏱  Time: {duration:.2f}s")
        print(f"   📊 Confidence: {confidence:.2%}")
        
        return {
            'success': True,
            'text': translated_text,
            'service': service_used,
            'fallback': is_fallback,
            'duration': duration,
            'confidence': confidence
        }
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"   ✗ Error: {str(e)}")
        print(f"   ⏱  Time: {duration:.2f}s")
        
        return {
            'success': False,
            'error': str(e),
            'duration': duration
        }


def run_tests():
    """Run comprehensive translation tests."""
    print_header("HYBRID TRANSLATION SYSTEM TEST")
    
    # Print configuration
    print_config()
    
    # Get translation service
    print_header("SERVICE INITIALIZATION")
    try:
        translator = ModelFactory.get_translation_service()
        
        # Check if it's a HybridTranslator
        if isinstance(translator, HybridTranslator):
            print("✓ HybridTranslator initialized")
            print(f"  Groq available: {translator.groq_available}")
            print(f"  HF available: {translator.hf_available}")
        else:
            print(f"⚠ Using {type(translator).__name__} (not hybrid mode)")
            
    except Exception as e:
        print(f"✗ Failed to initialize translator: {e}")
        return
    
    # Test cases
    test_cases = [
        # Kikuyu translations (should use HF)
        {
            'text': 'Wĩ mwega',
            'source': 'kikuyu',
            'target': 'english',
            'expected_service': 'hf',
            'description': 'Kikuyu → English (expects HF NLLB)'
        },
        {
            'text': 'Good morning',
            'source': 'english',
            'target': 'kikuyu',
            'expected_service': 'hf',
            'description': 'English → Kikuyu (expects HF NLLB)'
        },
        
        # Swahili translations (should use Groq if available, else HF)
        {
            'text': 'Habari yako',
            'source': 'swahili',
            'target': 'english',
            'expected_service': 'groq',  # or 'hf' if no Groq key
            'description': 'Swahili → English (expects Groq if key provided)'
        },
        {
            'text': 'How are you',
            'source': 'english',
            'target': 'swahili',
            'expected_service': 'groq',  # or 'hf' if no Groq key
            'description': 'English → Swahili (expects Groq if key provided)'
        },
        
        # Additional test cases
        {
            'text': 'Nĩ ũrĩa gwĩkĩrwo nĩ andũ othe marĩ na ũhoro wa kĩama',
            'source': 'kikuyu',
            'target': 'english',
            'expected_service': 'hf',
            'description': 'Complex Kikuyu sentence (expects HF)'
        },
    ]
    
    # Run tests
    print_header("RUNNING TESTS")
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[Test {i}/{len(test_cases)}] {test_case['description']}")
        
        result = test_translation(
            translator,
            test_case['text'],
            test_case['source'],
            test_case['target']
        )
        
        # Check if service matches expectation
        if result['success']:
            expected = test_case['expected_service']
            actual = result['service']
            
            # Allow 'hf' when Groq is expected but not available
            if expected == 'groq' and actual == 'hf' and not translator.groq_available:
                print(f"   ℹ  Using HF (Groq not available)")
                result['matched_expectation'] = True
            elif actual == expected:
                result['matched_expectation'] = True
            else:
                print(f"   ⚠  Expected {expected.upper()}, got {actual.upper()}")
                result['matched_expectation'] = False
        
        results.append({
            'test_case': test_case,
            'result': result
        })
    
    # Print summary
    print_header("TEST SUMMARY")
    
    successful = sum(1 for r in results if r['result']['success'])
    failed = len(results) - successful
    matched = sum(1 for r in results if r['result'].get('matched_expectation', False))
    
    print(f"📊 Total tests: {len(results)}")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"🎯 Matched expectations: {matched}/{successful}")
    
    if successful > 0:
        avg_time = sum(r['result']['duration'] for r in results if r['result']['success']) / successful
        avg_conf = sum(r['result']['confidence'] for r in results if r['result']['success']) / successful
        print(f"⏱  Average time: {avg_time:.2f}s")
        print(f"📊 Average confidence: {avg_conf:.2%}")
    
    # Service usage breakdown
    print(f"\n🔀 Service Usage:")
    groq_count = sum(1 for r in results if r['result'].get('service') == 'groq')
    hf_count = sum(1 for r in results if r['result'].get('service') == 'hf')
    fallback_count = sum(1 for r in results if r['result'].get('fallback', False))
    
    print(f"   Groq: {groq_count} translations")
    print(f"   HF: {hf_count} translations")
    if fallback_count > 0:
        print(f"   Fallbacks: {fallback_count}")
    
    # Print recommendations
    print_header("RECOMMENDATIONS")
    
    if not translator.groq_available and 'swahili' in settings.SUPPORTED_LANGUAGES:
        print("💡 Groq API not available. To enable faster Swahili translation:")
        print("   1. Get free API key: https://console.groq.com/keys")
        print("   2. Add to .env: GROQ_API_KEY=gsk_xxx")
        print("   3. Restart server")
        print("   Benefits: 3-5x faster Swahili translation, 30 req/min free tier")
    
    if not translator.hf_available:
        print("⚠️  HuggingFace API not available. This is required for Kikuyu:")
        print("   1. Get token: https://huggingface.co/settings/tokens")
        print("   2. Add to .env: HF_TOKEN=hf_xxx")
        print("   3. Restart server")
    
    if translator.groq_available and translator.hf_available:
        print("✅ Hybrid system fully operational!")
        print("   - Swahili: Using Groq (fast & accurate)")
        print("   - Kikuyu: Using HF NLLB (trained on Kikuyu data)")
        print("   - Fallback enabled for reliability")
    
    print()


if __name__ == '__main__':
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
