"""
Simple model loading test script.
Tests that all models can be loaded successfully.

Usage:
    python test_model_loading.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

import torch
from translation.services.huggingface_asr import HuggingFaceASR
from translation.services.nllb_translator import NLLBTranslator
from translation.services.mms_tts import MMSTTS


def test_model_loading():
    """Test that all models can be loaded."""
    print("\n" + "=" * 70)
    print("  Model Loading Test")
    print("=" * 70 + "\n")
    
    # Check device
    device = "GPU (CUDA)" if torch.cuda.is_available() else "CPU"
    print(f"Device: {device}\n")
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }
    
    # Test ASR models
    print("Testing ASR Models:")
    print("-" * 70)
    asr = HuggingFaceASR()
    
    for lang in ['kikuyu', 'swahili', 'english']:
        results['total'] += 1
        try:
            print(f"  [{lang.upper()}] Loading {asr.model_configs[lang]}...")
            asr._load_model(lang)
            
            # Check if model is loaded
            if lang in asr.models and lang in asr.processors:
                print(f"  ✓ {lang.upper()} ASR model loaded successfully")
                results['passed'] += 1
            else:
                print(f"  ✗ {lang.upper()} ASR model failed to load")
                results['failed'] += 1
                
        except Exception as e:
            print(f"  ✗ {lang.upper()} ASR model error: {str(e)}")
            results['failed'] += 1
        print()
    
    # Test Translation model
    print("\nTesting Translation Model:")
    print("-" * 70)
    results['total'] += 1
    
    try:
        translator = NLLBTranslator()
        print(f"  Loading {translator.model_name}...")
        translator._load_model()
        
        if translator.model is not None and translator.tokenizer is not None:
            print(f"  ✓ NLLB translation model loaded successfully")
            results['passed'] += 1
        else:
            print(f"  ✗ NLLB translation model failed to load")
            results['failed'] += 1
            
    except Exception as e:
        print(f"  ✗ NLLB translation error: {str(e)}")
        results['failed'] += 1
    print()
    
    # Test TTS models
    print("\nTesting TTS Models:")
    print("-" * 70)
    tts = MMSTTS()
    
    for lang in ['kikuyu', 'swahili', 'english']:
        results['total'] += 1
        try:
            print(f"  [{lang.upper()}] Loading {tts.model_configs[lang]}...")
            tts._load_model(lang)
            
            if lang in tts.models and lang in tts.tokenizers:
                print(f"  ✓ {lang.upper()} TTS model loaded successfully")
                results['passed'] += 1
            else:
                print(f"  ✗ {lang.upper()} TTS model failed to load")
                results['failed'] += 1
                
        except Exception as e:
            print(f"  ✗ {lang.upper()} TTS error: {str(e)}")
            results['failed'] += 1
        print()
    
    # Print summary
    print("=" * 70)
    print("  Test Summary")
    print("=" * 70)
    print(f"  Total:  {results['total']}")
    print(f"  Passed: {results['passed']} ✓")
    print(f"  Failed: {results['failed']} ✗")
    print(f"  Success Rate: {results['passed']/results['total']*100:.1f}%")
    print("=" * 70 + "\n")
    
    return results['failed'] == 0


if __name__ == "__main__":
    success = test_model_loading()
    sys.exit(0 if success else 1)
