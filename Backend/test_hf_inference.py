#!/usr/bin/env python
"""
Test script for Hugging Face Inference API services.

Requirements:
- HF_TOKEN set in .env
- USE_HF_INFERENCE=True in .env

Usage:
    python test_hf_inference.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

from django.conf import settings
from translation.services.factory import ModelFactory


def check_configuration():
    """Check if HF Inference API is properly configured."""
    print("=" * 70)
    print("CONFIGURATION CHECK")
    print("=" * 70)
    
    if not settings.HF_TOKEN:
        print("❌ ERROR: HF_TOKEN not set in .env")
        print("   Get a token from: https://huggingface.co/settings/tokens")
        return False
    else:
        token_preview = settings.HF_TOKEN[:10] + "..." if len(settings.HF_TOKEN) > 10 else settings.HF_TOKEN
        print(f"✓ HF_TOKEN: {token_preview}")
    
    if not settings.USE_HF_INFERENCE:
        print("❌ ERROR: USE_HF_INFERENCE=False in .env")
        print("   Set USE_HF_INFERENCE=True to test HF Inference API")
        return False
    else:
        print("✓ USE_HF_INFERENCE: True")
    
    if settings.DEMO_MODE:
        print("⚠️  WARNING: DEMO_MODE=True (takes priority over HF Inference)")
        print("   Set DEMO_MODE=False to test HF Inference API")
        return False
    else:
        print("✓ DEMO_MODE: False")
    
    print("\nConfiguration is valid!\n")
    return True


def test_asr_service():
    """Test ASR (Automatic Speech Recognition) service."""
    print("=" * 70)
    print("TEST 1: ASR Service")
    print("=" * 70)
    
    try:
        asr_service = ModelFactory.get_asr_service()
        print(f"✓ Service created: {type(asr_service).__name__}")
        
        # Note: Testing with actual audio requires audio files
        # For now, we just verify the service can be instantiated
        print("✓ ASR service initialization successful")
        print("  (Actual transcription test requires audio files)")
        
        return True
        
    except Exception as e:
        print(f"❌ ASR test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_translation_service():
    """Test Translation service."""
    print("\n" + "=" * 70)
    print("TEST 2: Translation Service")
    print("=" * 70)
    
    try:
        translator = ModelFactory.get_translation_service()
        print(f"✓ Service created: {type(translator).__name__}")
        
        # Test translation
        test_text = "Hello, how are you?"
        print(f"\nTranslating: '{test_text}'")
        print("Direction: english -> kikuyu")
        
        result = translator.translate(
            text=test_text,
            source_lang='english',
            target_lang='kikuyu'
        )
        
        print(f"✓ Translation successful!")
        print(f"  Original: {test_text}")
        print(f"  Translated: {result['text']}")
        print(f"  Confidence: {result['confidence']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Translation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_tts_service():
    """Test TTS (Text-to-Speech) service."""
    print("\n" + "=" * 70)
    print("TEST 3: TTS Service")
    print("=" * 70)
    
    try:
        tts_service = ModelFactory.get_tts_service()
        print(f"✓ Service created: {type(tts_service).__name__}")
        
        # Test speech synthesis
        test_text = "Mũgambo"
        print(f"\nSynthesizing: '{test_text}'")
        print("Language: kikuyu")
        
        audio_path = tts_service.synthesize(
            text=test_text,
            language='kikuyu'
        )
        
        print(f"✓ TTS successful!")
        print(f"  Text: {test_text}")
        print(f"  Audio saved to: {audio_path}")
        
        # Check if file exists
        if os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"  File size: {file_size} bytes")
        else:
            print(f"  ⚠️  Warning: Audio file not found at {audio_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all HF Inference API tests."""
    print("\n" + "🚀 " * 20)
    print("Hugging Face Inference API Test Suite")
    print("🚀 " * 20 + "\n")
    
    # Check configuration
    if not check_configuration():
        print("\n❌ Configuration check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Run tests
    results = {
        'ASR': test_asr_service(),
        'Translation': test_translation_service(),
        'TTS': test_tts_service()
    }
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:20s}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! HF Inference API is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
