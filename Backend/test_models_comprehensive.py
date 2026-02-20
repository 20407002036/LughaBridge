"""
Comprehensive test script for LughaBridge translation models.
Tests ASR, Translation, and TTS services with sample inputs.

Usage:
    python manage.py shell < test_models_comprehensive.py
    # OR
    python test_models_comprehensive.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lughabridge.settings')
django.setup()

import numpy as np
import scipy.io.wavfile as wavfile
from translation.services.huggingface_asr import HuggingFaceASR
from translation.services.nllb_translator import NLLBTranslator
from translation.services.mms_tts import MMSTTS


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def generate_test_audio(output_path, duration=3, sample_rate=16000, frequency=440):
    """
    Generate a simple test audio file (sine wave).
    
    Args:
        output_path: Where to save the audio
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        frequency: Frequency of the sine wave
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Save as WAV file
    wavfile.write(output_path, sample_rate, audio_data)
    print(f"✓ Generated test audio: {output_path}")
    return output_path


def test_asr_service():
    """Test Automatic Speech Recognition service."""
    print_section("Testing ASR (Automatic Speech Recognition) Service")
    
    asr_service = HuggingFaceASR()
    languages = ['kikuyu', 'swahili', 'english']
    
    # Create temp directory for test audio
    temp_dir = os.path.join(os.path.dirname(__file__), 'media', 'test_audio')
    os.makedirs(temp_dir, exist_ok=True)
    
    for lang in languages:
        print(f"\n--- Testing ASR for {lang.upper()} ---")
        
        try:
            # Test 1: Load model
            print(f"1. Loading {lang} ASR model...")
            asr_service._load_model(lang)
            print(f"   ✓ Model loaded successfully")
            print(f"   - Model: {asr_service.model_configs[lang]}")
            print(f"   - Device: {'GPU (CUDA)' if next(asr_service.models[lang].parameters()).is_cuda else 'CPU'}")
            
            # Test 2: Generate test audio
            print(f"\n2. Generating test audio...")
            test_audio_path = os.path.join(temp_dir, f'test_{lang}.wav')
            generate_test_audio(test_audio_path, duration=2)
            
            # Test 3: Transcribe (note: this will likely produce gibberish since we're using synthetic audio)
            print(f"\n3. Testing transcription...")
            print(f"   Note: Using synthetic audio, so output may not be meaningful")
            result = asr_service.transcribe(test_audio_path, lang)
            print(f"   ✓ Transcription completed")
            print(f"   - Text: '{result['text']}'")
            print(f"   - Confidence: {result['confidence']}")
            
            # Clean up test audio
            if os.path.exists(test_audio_path):
                os.remove(test_audio_path)
            
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n✓ ASR service tests completed")


def test_translation_service():
    """Test Translation service."""
    print_section("Testing NLLB Translation Service")
    
    translator = NLLBTranslator()
    
    # Test sentences in different languages
    test_cases = [
        {
            'text': 'Hello, how are you today?',
            'source': 'english',
            'target': 'swahili',
            'expected_contains': ['habari', 'uko', 'leo']  # Common Swahili words
        },
        {
            'text': 'Good morning, my friend.',
            'source': 'english',
            'target': 'kikuyu',
        },
        {
            'text': 'Habari za asubuhi?',
            'source': 'swahili',
            'target': 'english',
        },
        {
            'text': 'Jambo! Ninaitwa John.',
            'source': 'swahili',
            'target': 'english',
        },
    ]
    
    try:
        # Test 1: Load model
        print("1. Loading NLLB translation model...")
        translator._load_model()
        print("   ✓ Model loaded successfully")
        print(f"   - Model: {translator.model_name}")
        print(f"   - Device: {'GPU (CUDA)' if next(translator.model.parameters()).is_cuda else 'CPU'}")
        print(f"   - Supported languages: {', '.join(translator.lang_codes.keys())}")
        
        # Test 2: Translate sample texts
        print("\n2. Testing translations...\n")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"   Test {i}:")
            print(f"   - Source ({test_case['source']}): {test_case['text']}")
            
            result = translator.translate(
                test_case['text'],
                test_case['source'],
                test_case['target']
            )
            
            print(f"   - Target ({test_case['target']}): {result['text']}")
            print(f"   - Confidence: {result['confidence']}")
            print()
        
        print("✓ Translation service tests completed")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def test_tts_service():
    """Test Text-to-Speech service."""
    print_section("Testing MMS-TTS (Text-to-Speech) Service")
    
    tts_service = MMSTTS()
    
    # Test sentences
    test_cases = [
        {
            'text': 'Hello everyone, welcome to LughaBridge.',
            'language': 'english',
        },
        {
            'text': 'Habari yenu wote, karibu LughaBridge.',
            'language': 'swahili',
        },
        {
            'text': 'Wĩ mwega.',
            'language': 'kikuyu',
        },
    ]
    
    for lang_case in test_cases:
        lang = lang_case['language']
        text = lang_case['text']
        
        print(f"\n--- Testing TTS for {lang.upper()} ---")
        
        try:
            # Test 1: Load model
            print(f"1. Loading {lang} TTS model...")
            tts_service._load_model(lang)
            print(f"   ✓ Model loaded successfully")
            print(f"   - Model: {tts_service.model_configs[lang]}")
            print(f"   - Device: {'GPU (CUDA)' if next(tts_service.models[lang].parameters()).is_cuda else 'CPU'}")
            
            # Test 2: Synthesize speech
            print(f"\n2. Synthesizing speech...")
            print(f"   - Input text: '{text}'")
            
            audio_path = tts_service.synthesize(text, lang)
            
            print(f"   ✓ Speech synthesized successfully")
            print(f"   - Output file: {audio_path}")
            
            # Check file properties
            if os.path.exists(audio_path):
                file_size = os.path.getsize(audio_path)
                print(f"   - File size: {file_size:,} bytes")
                
                # Read audio to get duration
                sample_rate, audio_data = wavfile.read(audio_path)
                duration = len(audio_data) / sample_rate
                print(f"   - Duration: {duration:.2f} seconds")
                print(f"   - Sample rate: {sample_rate} Hz")
            
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n✓ TTS service tests completed")


def test_full_pipeline():
    """Test full translation pipeline: TTS -> ASR -> Translation -> TTS."""
    print_section("Testing Full Translation Pipeline")
    
    print("Testing: Text -> TTS -> ASR -> Translation")
    print("Note: This tests the integration of all services\n")
    
    try:
        # Initialize services
        tts_service = MMSTTS()
        asr_service = HuggingFaceASR()
        translator = NLLBTranslator()
        
        # Test case: English text -> English audio -> transcribe -> translate to Swahili
        original_text = "Hello, how are you?"
        source_lang = "english"
        target_lang = "swahili"
        
        print(f"1. Original text ({source_lang}): '{original_text}'")
        
        # Step 1: Text to Speech
        print(f"\n2. Converting text to speech ({source_lang})...")
        audio_path = tts_service.synthesize(original_text, source_lang)
        print(f"   ✓ Audio generated: {audio_path}")
        
        # Step 2: Speech to Text (ASR)
        print(f"\n3. Transcribing audio back to text...")
        transcription_result = asr_service.transcribe(audio_path, source_lang)
        print(f"   ✓ Transcribed text: '{transcription_result['text']}'")
        print(f"   - Confidence: {transcription_result['confidence']}")
        
        # Step 3: Translate
        print(f"\n4. Translating to {target_lang}...")
        translation_result = translator.translate(
            transcription_result['text'],
            source_lang,
            target_lang
        )
        print(f"   ✓ Translated text: '{translation_result['text']}'")
        print(f"   - Confidence: {translation_result['confidence']}")
        
        # Step 4: Convert translation to speech
        print(f"\n5. Converting translation to speech ({target_lang})...")
        translated_audio = tts_service.synthesize(translation_result['text'], target_lang)
        print(f"   ✓ Audio generated: {translated_audio}")
        
        print("\n✓ Full pipeline test completed successfully!")
        print("\nPipeline summary:")
        print(f"  Input:  '{original_text}' ({source_lang})")
        print(f"  Output: '{translation_result['text']}' ({target_lang})")
        
    except Exception as e:
        print(f"\n✗ Pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()


def print_summary():
    """Print test summary and model information."""
    print_section("Test Summary")
    
    print("Models tested:")
    print("\nASR Models:")
    print("  - Kikuyu:  badrex/w2v-bert-2.0-kikuyu-asr")
    print("  - Swahili: thinkKenya/wav2vec2-large-xls-r-300m-sw")
    print("  - English: facebook/wav2vec2-large-960h-lv60-self")
    
    print("\nTranslation Model:")
    print("  - NLLB: facebook/nllb-200-distilled-600M")
    
    print("\nTTS Models:")
    print("  - Kikuyu:  facebook/mms-tts-kik")
    print("  - Swahili: facebook/mms-tts-swh")
    print("  - English: facebook/mms-tts-eng")
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80 + "\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("  LughaBridge Model Testing Suite")
    print("=" * 80)
    
    try:
        # Test each service
        test_asr_service()
        test_translation_service()
        test_tts_service()
        
        # Test full pipeline
        test_full_pipeline()
        
        # Print summary
        print_summary()
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
